from application.workers import celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from application.models import *
import csv
import os
from application.email_config import send_email
from flask import render_template_string
from flask import current_app
from weasyprint import HTML

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        #crontab(minute=0, hour=21),
        crontab(),
        daily_reminder.s(),
        name='daily reminder'
    )

    sender.add_periodic_task(
        crontab(0,0,day_of_month='1'),
        #crontab(),
        monthly_report.s(),
        name='monthly report'
    )


   
@celery.task()
def daily_reminder():
    threshold_time = datetime.utcnow() - timedelta(hours=2) #minutes=2 for checking, for now works perfectly

    inactive_users = User.query.filter(User.last_visited_time < threshold_time).all()

    if not inactive_users:
        print("No inactive users to remind.")
        return "No inactive users"
    
    for user in inactive_users:
        message='Hello, '+user.user_name+'! This is a reminder daily remainder to check out the Upcoming Quizzes.'
        send_email(to=user.user_email,sub= 'Your Daily Reminder',message=message)
        print("DAILY_REMINDER") 

    print(f"Sent reminders to {len(inactive_users)} inactive users.")
    return f"Reminders sent to {len(inactive_users)} users"
 


@celery.task()
def monthly_report():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    users=User.query.all()

    if not users:
        return "No users fornd for monthly report"
    
    for user in users:
        user_scores=Score.query.filter(
            Score.user_id==user.id,
            Score.time_of_attempt>= datetime(current_year, current_month, 1),
            Score.time_of_attempt < datetime(current_year, current_month+1, 1)
        ).all()

        if not user_scores:
            continue    
    
        total_quizzes=len(user_scores)
        total_score=sum(score.total_score for score in user_scores)
        avg_score=total_score/ total_quizzes if total_quizzes> 0 else 0


        report_html=render_template_string("""
            <html>
            <body>
                <h2>Monthly Activity Report - {{ month }}/{{ year }}</h2>
                    <p>Hello {{ name }},</p>
                    <p>Here's your activity summary for this month:</p>
                    <ul>
                        <li>Total Quizzes Attempted: {{ total_quizzes }}</li>
                        <li>Average Score: {{ avg_score }}</li>
                    </ul>
                    <p>Keep up the good work!</p>
                </body>
            </html>  

        """, name=user.user_name, month=current_month, year=current_year, total_quizzes=total_quizzes, avg_score=round(avg_score,2))
        

        
        EXPORT_DIR = "exported_files"
        os.makedirs(EXPORT_DIR, exist_ok=True)

        pdf_file_name = f"monthly_report_{user.id}_{current_month}_{current_year}.pdf"
        pdf_path = os.path.join(EXPORT_DIR, pdf_file_name)
        HTML(string=report_html).write_pdf(pdf_path)
        

        send_email(to=user.user_email, 
                    sub='Your Monthly Activity Report',
                    message=report_html                
        )
    return "Monthly reports sent to active users"
 


# USER KA
@celery.task(bind=True)
def export_quiz_results(self, user_id):
    self.update_state(state="STARTED")

    user = User.query.get(user_id)
    if not user:
        self.update_state(state="FAILURE", meta={"error": f"User {user_id} not found"})
        return {"status": "failed", "error": f"User {user_id} not found"}

    user_scores = Score.query.filter(Score.user_id == user_id).all()
    if not user_scores:
        email_body = f"""
            <html>
            <body>
                <p>Hello {user.user_name},</p>
                <p>There is no quiz data available to export for your profile.</p>
                <p>Regards,</p>
                <p>Quizzy Admin</p>
            </body>
            </html>
        """
        send_email(to=user.user_email, sub="No Quiz Data Available", message=email_body)
        return f"No quiz data for {user.user_name}, email sent."
     
    file_name = f"quiz_results_of_USERID_{user_id}.csv"   
    file_path = os.path.join("exported_files", file_name)

    os.makedirs("exported_files", exist_ok=True)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Quiz ID", "Quiz Name", "Chapter ID", "Date of Quiz", "Score", "Remarks"])

        for score in user_scores:
            quiz = Quiz.query.get(score.quiz_id)
            chapter = Chapter.query.get(quiz.chapter_id) if quiz else None
            remarks = "Good" if score.total_score >= 50 else "Needs Improvement" # MODIFY later

            writer.writerow([
                quiz.id if quiz else "N/A",
                quiz.quiz_name if quiz else "Unknown",
                chapter.id if chapter else "N/A",
                quiz.date_of_quiz if quiz else "N/A",
                score.total_score,
                remarks
            ])
    
    download_link = f"http://localhost:8080/download_csv/{file_name}"
    email_body = f"""
        <html>
        <body>
            <p>Hello {user.user_name},</p>
            <p>Your quiz results export is ready! Click the link below to download:</p>
            <a href="{download_link}">Download CSV</a>
            <p>Regards,</p>
            <p>QUIZZY ADMIN.</p>
        </body>
        </html>
    """
    send_email(to=user.user_email, sub="Your Quiz Results Export", message=email_body)

    self.update_state(state='SUCCESS', meta={'csv_url': download_link}) # save file url 

    return f"CSV exported for {user.user_name} and email sent."


# ADMIN KA
@celery.task(bind=True)
def export_all_users_quiz_data(self, admin_id):
    self.update_state(state="STARTED")

    job_id = self.request.id  # Celery task ID
    file_name = f"all_users_quiz_data_{job_id}.csv"
    file_path = os.path.join("exported_files", file_name)
    os.makedirs("exported_files", exist_ok=True)
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "User Name", "Total Quizzes Taken", "Average Score"])
        
        users = User.query.all()
        for user in users:
            quizzes_taken = Score.query.filter_by(user_id=user.id).count()
            avg_score = db.session.query(db.func.avg(Score.total_score)).filter(Score.user_id == user.id).scalar()
            avg_score = round(avg_score, 2) if avg_score else 0

            writer.writerow([user.id, user.user_name, quizzes_taken, avg_score])
    
    download_link = f"http://localhost:8080/download_csv/{file_name}"
    
    self.update_state(state='SUCCESS', meta={'csv_url': download_link})
    return {"csv_url": download_link}



       


