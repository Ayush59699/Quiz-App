from flask import Flask,request
from sqlalchemy import func
from flask_login import LoginManager
from application.models import *
import os, uuid
from datetime import datetime, date
from flask import request, jsonify
from flask import current_app as app
from flask import request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, get_jwt
import random
from application import workers
from application.workers import celery
from application.cache import cache 
from flask_cors import CORS
import requests
from application.tasks import *
from flask import send_file
from dotenv import load_dotenv
 
load_dotenv() 


AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN= os.getenv('AIPROXY_TOKEN')





@app.route('/generate_ai_content', methods=['POST'])
@jwt_required()
def generate_ai_content():
    data = request.json
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": f"Generate a long summary about {topic}"}]
    }

    try:
        response = requests.post(AIPROXY_URL, headers=headers, json=payload)
        ai_response = response.json()

        # Extract AI-generated content
        content = ai_response.get("choices", [{}])[0].get("message", {}).get("content", "")

        return jsonify({"topic": topic, "content": content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export_quiz_csv", methods=["POST"])
@jwt_required()
def trigger_quiz_export():
    """ User clicks 'Export' → Starts async job """
    try:
        user_id = get_jwt_identity()
        user_id=uuid.UUID(user_id)

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404        
        task=export_quiz_results.apply_async(args=[user_id])
        print("CELERY TASK ID IS :", task.id)

        return jsonify({"message": "Your export is in progress. You will receive an email when it’s ready!",
                        "job_id":task.id}), 202

    except ValueError as e:
        return jsonify({'error': str(e)}),500


@app.route('/download_report/<user_id>', methods=['GET'])
def download_report(user_id):
    try:
        user_id=uuid.UUID(user_id)
        print(user_id)
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        EXPORT_DIR = "exported_files"
        pdf_file_name = f"monthly_report_{user_id}_{current_month}_{current_year}.pdf"
        pdf_path = os.path.join(EXPORT_DIR, pdf_file_name)
        
        if os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True)
        else:
            return jsonify({"error": "Report not found"}), 404

    except ValueError as e:
        return jsonify({'error':e})


# BOTH ADMIN AND USER
@app.route("/download_csv/<filename>", methods=["GET"])
def download_csv(filename):
    file_path = os.path.join("exported_files", filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)


# Check the status of a quiz export job.
@app.route("/export_status/<job_id>", methods=["GET"])
def export_status(job_id):    
    task = celery.AsyncResult(job_id)  # Fetch the task status from Celery
    if task.state == "PENDING":
        return jsonify({"status": "pending"}), 202
    elif task.state == "FAILURE":
        return jsonify({"status": "failed"}), 500
    elif task.state == "SUCCESS":
        if task.result and isinstance(task.result, dict):
            csv_url=task.result.get('csv_url')
            return jsonify({"status": "completed", "csv_url": csv_url}), 200
        return jsonify({"status": "failed", "message": "CSV file not found"}), 500          
    else:
        return jsonify({"status": task.state}), 202


##  ADMIN PART
@app.route("/admin_export_quiz_csv", methods=["POST"])
@jwt_required()
def trigger_admin_quiz_export():
    """ User clicks 'Export' → Starts async job """
    try:
        admin_id = get_jwt_identity()
        admin_id=uuid.UUID(admin_id)

        admin = Admin.query.get(admin_id)

        if not admin:
            return jsonify({"error": "Admin not found"}), 404    
            
        task=export_all_users_quiz_data.apply_async(args=[admin_id]) 

        print("CELERY TASK ID IS :", task.id)

        return jsonify({"message": "Your export is in progress. You will receive an email when it’s ready!",
                        "job_id":task.id}), 202

    except ValueError as e:
        return jsonify({'error': str(e)}),500



@app.route('/edit_quiz', methods=['PUT'])
@jwt_required()
def edit_quiz():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    
    data = request.json
    quiz_id = data.get('id')
    if not quiz_id:
        return jsonify({'error': 'Quiz ID is required'}), 400
    
    try:
        if not isinstance(quiz_id, uuid.UUID):  
            quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        return jsonify({'error': 'Invalid Quiz ID format'}), 400
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    # Update fields if provided
    if 'quiz_name' in data:
        quiz.quiz_name = data['quiz_name']
    if 'date_of_quiz' in data:
        try:
            quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if 'time_duration' in data:
        if not isinstance(data['time_duration'], int) or data['time_duration'] <= 0:
            return jsonify({'error': 'Time duration must be a positive integer'}), 400
        quiz.time_duration = data['time_duration']

    db.session.commit()
    return jsonify({'message': 'Quiz updated successfully', 'quiz': quiz.to_json()}), 200


@app.route('/delete_quiz/<string:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    try:
        quiz_uuid = uuid.UUID(quiz_id) 
    except ValueError:
        return jsonify({'message': 'Invalid quiz ID format'}), 400  

    quiz = Quiz.query.get(quiz_uuid)

    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    # Delete all associated questions first
    Question.query.filter_by(quiz_id=quiz_uuid).delete()

    # Now delete the quiz
    db.session.delete(quiz)
    db.session.commit()

    return jsonify({'message': 'Quiz deleted successfully'}), 200


@app.route("/user/change_password", methods=["POST"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user_id=uuid.UUID(user_id)

    data = request.get_json()

    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "New password is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.user_password = new_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"})


@app.route("/user/set_reminder", methods=["POST"]) ## BACHA HUA HAI
@jwt_required()
def set_reminder():
    token = get_jwt()
    if not token['type'] == 'user':
        return {'message': 'Now allowed to access this page, login as user'}, 401
    user_id = get_jwt_identity()
    user_id=uuid.UUID(user_id)

    data = request.get_json()
    
    reminder_time_str = data.get("reminder_time")
    if not reminder_time_str:
        return jsonify({"error": "Reminder time is required from API"}), 400

    try:    
        reminder_time=datetime.strptime(reminder_time_str, "%H:%M").time()
        reminder_datetime = datetime.combine(date.today(), reminder_time)  # Convert to full datetime
    
    except ValueError:
        return jsonify({'error':'Invalid date format hai'})

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.reminder_time = reminder_datetime
    db.session.commit()

    return jsonify({"message": f"Reminder set for {reminder_time}!"})


@app.route('/get_user_profile_details', methods=['GET','PUT'])
@jwt_required()
@cache.memoize(timeout=60)
def get_user_profile_details():
    
    user_id = get_jwt_identity()
    user_id=uuid.UUID(user_id)
    
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({
            "user_id": user_id,
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_qualification": user.user_qualification,
            "user_dob": user.user_dob,
            "last_visited_time": user.last_visited_time
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        user.user_name = data.get("user_name", user.user_name)
        user.user_qualification = data.get("user_qualification", user.user_qualification)
        user.user_dob = data.get("user_dob", user.user_dob)

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200


@app.route('/user_dashboard', methods=["GET", 'POST'])
@jwt_required()
@cache.memoize(timeout=60)
def user_dashboard():
    token = get_jwt()
    if not token['type'] == 'user':
        return {'message': 'Only Users are allowed to access this page, login as User'}, 401

    #upcoming_quizzes = Quiz.query.filter(Quiz.date_of_quiz >= date.today()).all()
    all_quizzes = Quiz.query.all()
    active_quizzes = [quiz.to_json() for quiz in all_quizzes if quiz.date_of_quiz >= date.today()]
    expired_quizzes = [quiz.to_json() for quiz in all_quizzes if quiz.date_of_quiz < date.today()]
    
    return jsonify({
        "active_quizzes": active_quizzes,
        "expired_quizzes": expired_quizzes
    }), 200




@app.route('/user_leaderboard', methods=["GET", 'POST'])
@jwt_required()
@cache.memoize(timeout=160)
def user_leaderboard():
    user_id = get_jwt_identity()  # Get logged-in user ID
    user_id=uuid.UUID(user_id)

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    # Get leaderboard data (Users ranked by total score)
    leaderboard_data = (
        db.session.query(User.user_name, func.sum(Score.total_score).label("total_score"))
        .join(Score, User.id == Score.user_id)
        .group_by(User.id)
        .order_by(func.sum(Score.total_score).desc())
        .limit(10)  # Top 10 users
        .all()
    )
    leaderboard = [
        {"user_name": entry.user_name, "total_score": entry.total_score}
        for entry in leaderboard_data
    ]
    return jsonify({"leaderboard": leaderboard}), 200



@app.route('/user_login', methods=["GET", 'POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            user_email = data.get('user_email')
            user_password = data.get('user_password')
            user_name= data.get('user_name','')
            user_qualification= data.get('user_qualification')
            user_dob= data.get('user_dob','')
            
            user_from_db = User.query.filter_by(user_email=user_email).first()
            
            if user_from_db:
                if user_from_db.user_password == user_password:

                    user_from_db.last_visited_time = datetime.utcnow()
                    db.session.commit()

                    token=create_access_token( identity=user_from_db.id, additional_claims={"type": "user", "id":user_name })
                                                #identity=admin_name
                    return {"access_token": token ,
                             'user_name': user_from_db.user_name, 
                            'user_email': user_from_db.user_email,}, 200
                else:
                    return {"message": "Wrong password"}, 401
            else:
                return {"message": "User Name is not correct"}, 404
        else:
            return "No data provided"
    return "Welcome to the User Home Page"


@app.route('/user_register', methods=["GET", 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            user_email = data.get('user_email')
            user_password = data.get('user_password')
            user_name= data.get('user_name')
            user_qualification= data.get('user_qualification')
            user_dob= data.get('user_dob')
        
        user_from_db=User.query.filter_by(user_email=user_email).first()
        if user_from_db:
            return {"message": "User already exists"}, 400
        
        new_user=User(user_email=user_email, user_password=user_password, user_name=user_name, user_qualification=user_qualification, user_dob=user_dob)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created"}, 200
    return "Welcome to the User Home Page"


@app.route('/quiz_management', methods=['GET'])
@jwt_required()
def view_all_quizzes():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as Admin'}, 401

    try:
        quizzes = Quiz.query.all()
        return jsonify([quiz.to_json() for quiz in quizzes]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_quiz', methods=['GET','POST'])
@jwt_required()
def add_quiz():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    try:
        data=request.get_json()
        chapter_id = data.get('chapter_id')
        quiz_name = data.get('quiz_name')
        date_of_quiz = data.get('date_of_quiz')
        time_duration = data.get('time_duration')

        if not (chapter_id and quiz_name and date_of_quiz and time_duration):
            return jsonify({"error": "All fields are required"}), 400
        
        date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

        new_quiz = Quiz(
            id=uuid.uuid4(),
            chapter_id=uuid.UUID(chapter_id),
            quiz_name=quiz_name,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration
        )
        db.session.add(new_quiz)
        db.session.commit()

        return jsonify({"message": "Quiz added successfully", "quiz_id": str(new_quiz.id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_get_chapters', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=60)
def get_get_chapters():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    chapters = Chapter.query.all()
    return jsonify([{"id": str(ch.id), "chapter_name": ch.chapter_name} for ch in chapters])


@app.route("/add_question", methods=['GET','POST'])
@jwt_required()
def add_question():
    token=get_jwt()
    if token['type']!= 'admin':
        return jsonify({'message': 'Not authorized'}), 401
    
    data=request.get_json()
    if not data:
        return jsonify({'message':'No data provided'}), 400
    
    
    quizid=data.get('quiz_id')
    print(f"Received quiz_id: {quizid}") 

    try:
        quizid=uuid.UUID(quizid)
    except ValueError:
        return jsonify({"message": "Invalid UUID format", "received": quizid}), 400

    quiz = db.session.get(Quiz, quizid)

    if not quiz:
        return jsonify({'message':'Quiz not found'}), 404
    
    try:
        new_question=Question(
            quiz_id=uuid.UUID(data.get('quiz_id')),
            question_statement=data['question_statement'],
            option1=data['option1'],
            option2=data['option2'],
            option3=data['option3'],
            option4=data['option4'],
            correct_option=data['correct_option']
        )
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'message':'Question added successfully', 'question': new_question.to_json()}), 201
    
    except ValueError:
        return jsonify({"message": "Invalid UUID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_chapter/<chapter_id>", methods=["GET"])
@jwt_required()
def get_chapter(chapter_id):
    try:
        chapter_id=(uuid.UUID(chapter_id))
        chapter = Chapter.query.get(chapter_id)

        if not chapter:
            return jsonify({"message": "Chapter not found"}), 404

        return jsonify({"chapter_name": chapter.chapter_name}), 200

    except ValueError:
        return jsonify({'message':'Invalid UUID format hai'}),400


@app.route('/take_quiz/<quiz_id>', methods=['GET','POST'])
@jwt_required()
def get_questions(quiz_id):
    try:
        quiz_id=(uuid.UUID(quiz_id))
        quiz=db.session.get(Quiz, quiz_id)
        if not quiz:
            return jsonify({'message': 'Quiz not found'}), 404
        
        questions=Question.query.filter_by(quiz_id=quiz_id).all()
        return jsonify(  {
            'questions':[q.to_json() for q in questions],
            'quiz_id': str(quiz.id),
            'quiz_name': quiz.quiz_name,
            'time_duration': quiz.time_duration,
            })

    except ValueError:
        return jsonify({'message':'Invalid UUID format hai'}),400
    

@app.route('/view_quiz_details/<string:quiz_id>', methods=["GET"])
@jwt_required() # its for both user and admin
def view_quiz_details(quiz_id):
    try:
        quiz_id=(uuid.UUID(quiz_id))
        quiz = Quiz.query.get(quiz_id)
    
        if not quiz:
            return jsonify({"message": "Quiz not found"}), 404
        
        quiz_details = {
            "quiz_name": quiz.quiz_name,
            'quiz_id': (quiz.id),
            "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
            "time_duration": quiz.time_duration,
            "chapter_id": quiz.chapter_id,
            "chapter_name": quiz.chapter.chapter_name,
            'subject_name': quiz.chapter.subject.subject_name,
        }
        return jsonify(quiz_details)

    except ValueError:
            return jsonify({'message':"Invalid UUID Format "}),400


@app.route('/manage_chapter_quizzes/<string:chapter_id>', methods=['GET'])
@jwt_required()
def manage_chapter_quizzes(chapter_id):
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as Admin'}, 401

    try:
        chapter_id=(uuid.UUID(chapter_id))
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

        if not quizzes:
            return jsonify({"message": "No Quizzes are found"}), 200
        
        #print(quizzes)
        return jsonify([quiz.to_json() for quiz in quizzes]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/edit_question/<string:question_id>', methods=['PUT'])
@jwt_required()
def edit_question(question_id):
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    data = request.json
    question_id=(uuid.UUID(question_id))
    question = Question.query.get(question_id)

    if not question:
        return jsonify({'message': 'Question not found'}), 404

    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)

    db.session.commit()
    return jsonify({'message': 'Question updated successfully', 'question': question.to_json()}), 200


@app.route('/delete_question/<string:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    question_id=uuid.UUID(question_id)
    question = Question.query.get(question_id)

    if not question:
        return jsonify({'message': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'}), 200


@app.route('/save_score', methods=['POST'])
@jwt_required()# saves the quiz score to DB
def save_score():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        quiz_id = data.get('quiz_id') 
        total_score = data.get('total_score')
        #print(f"Received quiz_id: {quiz_id} (Type: {type(quiz_id)})")  # Debugging
        quiz_id = quiz_id.strip()
        quiz_id = uuid.UUID(quiz_id)

        new_score = Score(
            user_id=uuid.UUID(user_id),
            quiz_id=quiz_id,
            time_of_attempt=datetime.utcnow(),
            total_score=total_score
        )
        db.session.add(new_score)
        db.session.commit()

        return jsonify({"message": "Score saved successfully"}), 201

    except ValueError as e:
        print(f"UUID Conversion Error: {e}")  
        return jsonify({"error": "Invalid quiz_id format"}), 400

    except Exception as e:
        print(f"Unexpected Error: {e}")  
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/my_attempts', methods=['POST', 'GET'])
@jwt_required()
@cache.memoize(timeout=60)
def user_attempts():
    token = get_jwt()
    if not token['type'] == 'user':
        return {'message': 'Now allowed to access this page, login as user'}, 401
    
    user_id = get_jwt_identity()
    user_id = uuid.UUID(user_id)

    # Fetch all attempts by the user
    attempts = db.session.query(
        Score.quiz_id, Quiz.quiz_name, Score.time_of_attempt, Score.total_score
    ).join(Quiz, Score.quiz_id == Quiz.id).filter(Score.user_id == user_id).all()

    # Fetch max scores for each quiz
    highest_scores = db.session.query(
        Score.quiz_id, func.max(Score.total_score).label('max_score')
    ).filter(Score.user_id == user_id).group_by(Score.quiz_id).all()

    # Convert max scores to a dictionary
    highest_scores_dict = {str(qid): max_score for qid, max_score in highest_scores}

    # Group attempts by quiz
    quiz_attempts_dict = {}
    for quiz_id, quiz_name, time_of_attempt, total_score in attempts:
        quiz_id_str = str(quiz_id)
        if quiz_id_str not in quiz_attempts_dict:
            quiz_attempts_dict[quiz_id_str] = {
                "quiz_id": quiz_id_str,
                "quiz_name": quiz_name,
                "highest_score": highest_scores_dict.get(quiz_id_str, total_score),
                "attempts": []
            }
        quiz_attempts_dict[quiz_id_str]["attempts"].append({
            "time_of_attempt": time_of_attempt.strftime("%Y-%m-%d %H:%M:%S"),
            "total_score": total_score
        })

    # Convert to list for JSON response
    return jsonify(list(quiz_attempts_dict.values())), 200


@app.route("/user/scores", methods=["GET"])
@jwt_required()
def get_scores():
    user_id = get_jwt_identity() 

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        user_uuid = uuid.UUID(user_id)  # Convert user_id to UUID
    except ValueError:
        return jsonify({"error": "Invalid User ID format"}), 400

    scores = Score.query.filter_by(user_id=user_uuid).all()

    return jsonify([score.to_json() for score in scores])


@app.route('/get_subject_wise_quiz_chart_data', methods=['GET','POST'])
@jwt_required()
@cache.memoize(timeout=60)
def get_subject_wise_quiz_chart_data():
    user_id=get_jwt_identity()
    user_id=uuid.UUID(user_id)

    subject_attempts = (
            db.session.query(
                Subject.subject_name,
                db.func.count(Score.id).label("attempt_count")
            )
            .join(Chapter, Subject.id == Chapter.subject_id)
            .join(Quiz, Chapter.id == Quiz.chapter_id)
            .join(Score, Quiz.id == Score.quiz_id)
            .filter(Score.user_id == user_id)
            .group_by(Subject.subject_name)
            .all()
        )

    # Convert results to a dictionary
    chart_data = {subject: count for subject, count in subject_attempts}

    return jsonify(chart_data)


from collections import defaultdict
@app.route('/get_month_wise_quiz_chart_data', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=60)
def get_month_wise_quiz_chart_data():
    scores = Score.query.all()
    month_attempts = defaultdict(int)

    for score in scores:
        month = score.time_of_attempt.strftime("%B %Y")  # Example: "March 2025"
        month_attempts[month] += 1

    return jsonify(month_attempts)


@app.route('/admin_summary', methods=["GET","POST"])
@jwt_required()
@cache.memoize(timeout=60)
def admin_summary():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    
    quizzes=db.session.query(
        Quiz.quiz_name, func.count(Score.id).label('attempt_count')
    ).join(Score, Quiz.id == Score.quiz_id).group_by(Quiz.quiz_name).all()
    
    return jsonify([{"quiz_name": quiz_name, "attempt_count": attempt_count} for quiz_name, attempt_count in quizzes])


@app.route('/admin_summary2', methods=["GET","POST"])
@jwt_required()
@cache.memoize(timeout=60)
def admin_summary2():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    
    top_scores = db.session.query(
        Subject.subject_name,
        func.max(Score.total_score).label('top_score')
    ).join(Chapter, Subject.id == Chapter.subject_id) \
    .join(Quiz, Chapter.id == Quiz.chapter_id) \
    .join(Score, Quiz.id == Score.quiz_id) \
    .group_by(Subject.subject_name) \
    .all()

    subject_scores = [{'subject_name': subject, 'top_score': score} for subject, score in top_scores]
    return jsonify(subject_scores)


@app.route('/admin_summary3', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=60)
def get_subject_attempts():
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    
    subject_attempts = db.session.query(
        Subject.subject_name,
        func.count(Score.id).label('attempt_count')
    ).join(Chapter, Subject.id == Chapter.subject_id) \
     .join(Quiz, Chapter.id == Quiz.chapter_id) \
     .join(Score, Quiz.id == Score.quiz_id) \
     .group_by(Subject.subject_name) \
     .all()

    # Convert the results into JSON format
    response_data = [{"subject_name": subject, "attempt_count": attempts} for subject, attempts in subject_attempts]

    return jsonify(response_data)


@app.route('/admin_login', methods=["GET", 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            admin_email = data.get('admin_email')
            admin_password = data.get('admin_password')
            admin_name= data.get('admin_name')
            admin_from_db = Admin.query.filter_by(admin_email=admin_email).first()
            if admin_from_db:
                if admin_from_db.admin_password == admin_password:
                    token=create_access_token( identity=admin_from_db.id, additional_claims={"type": "admin", "id":admin_name })
                                                #identity=admin_name
                    return {"access_token": token }, 200
                else:
                    return {"message": "Wrong password"}, 401
            else:
                return {"message": "Admin Name is not correct"}, 404
        else:
            return "No data provided"
    return "Welcome to the home page"


@app.route('/admin_dashboard', methods=["GET", 'POST'])
@jwt_required()
def admin_dashboard():    
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    users = User.query.all()  
    users_json = [user.to_json() for user in users]  
    
    subjects=Subject.query.all()
    chapters=Chapter.query.all()

    subjects_json = []
    for subject in subjects:
        sub_data=subject.to_json()
        sub_data['chapters']=[ chapter.to_json() for chapter in chapters if chapter.subject_id ==subject.id]
        subjects_json.append(sub_data)

    return jsonify({
        'users': users_json,
        'subjects': subjects_json,
    })


@app.route('/create_subject', methods=["POST"]) 
@jwt_required()
def create_subject():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    
    subject_name = data.get('subject_name')
    subject_description = data.get('subject_description', None)  
    
    if not subject_name:
        return {'message': 'Subject name is required'}, 400
        
    subject = Subject(subject_name=subject_name, subject_description=subject_description)
    db.session.add(subject)
    db.session.commit()
    return {"message": "Subject created successfully"}, 201


@app.route('/update_subject', methods=["PUT"])
@jwt_required()
def update_subject():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    
    subject_id = data.get('subject_id')    
    subject_name = data.get('subject_name')
    subject_description = data.get('subject_description', None)  
    
    if not subject_id:
        return {'message': 'Subject ID is required'}, 400
    
    try:
        subject_id = uuid.UUID(subject_id)
    except ValueError:
        return {'message': 'Invalid subject ID'}, 400
        
    subject = Subject.query.get(subject_id)
    if not subject:
        return {'message': 'Subject not found'}, 404
    
    if subject_name:
        subject.subject_name = subject_name
    if subject_description:
        subject.subject_description = subject_description
    
    db.session.commit()
    return {"message": "Subject updated successfully"}, 200


@app.route('/delete_subject', methods=["DELETE"])
@jwt_required()
def delete_subject():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    
    subject_id = data.get('subject_id')    
    if not subject_id:
        return {'message': 'Subject ID is required'}, 400
    
    try:
        subject_id = uuid.UUID(subject_id)
    except ValueError:
        return {'message': 'Invalid subject ID'}, 400
        
    subject = Subject.query.get(subject_id)
    if not subject:
        return {'message': 'Subject not found'}, 404
    
    db.session.delete(subject)
    db.session.commit()
    return {"message": "Subject deleted successfully"}, 200


@app.route('/create_chapter', methods=["POST",'GET'])
@jwt_required()
def create_chapter():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 401
    
    chapter_name = data.get('chapter_name')
    chapter_description = data.get('chapter_description', None)
    subject_id = data.get('subject_id')
    
    if not chapter_name:
        return {'message': 'Chapter name is required'}, 402
    if not subject_id:
        return {'message': 'Subject ID is required'}, 403
    
    try:
        subject_id = uuid.UUID(subject_id)
    except ValueError:
        return {'message': 'Invalid subject ID'}, 404
    
    subject = Subject.query.get(subject_id)
    if not subject:
        return {'message': 'Subject not found'}, 405
    
    chapter = Chapter(chapter_name=chapter_name, chapter_description=chapter_description, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()
    return {"message": "Chapter created successfully"}, 201


@app.route('/update_chapter', methods=["PUT"])
@jwt_required()
def update_chapter():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    
    chapter_id = data.get('chapter_id')
    chapter_name = data.get('chapter_name')
    chapter_description = data.get('chapter_description', None)
    
    if not chapter_id:
        return {'message': 'Chapter ID is required'}, 400
    
    try:
        chapter_id = uuid.UUID(chapter_id)
    except ValueError:
        return {'message': 'Invalid chapter ID'}, 400
        
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {'message': 'Chapter not found'}, 404
    
    if chapter_name:
        chapter.chapter_name = chapter_name
    if chapter_description:
        chapter.chapter_description = chapter_description
    
    db.session.commit()
    return {"message": "Chapter updated successfully"}, 200


@app.route('/delete_chapter', methods=["DELETE"])
@jwt_required()
def delete_chapter():
    token=get_jwt() 
    if not token['type']=='admin':
        return {'message': 'Only Admins are allowed to access this page, login as Admin'}, 401
    
    data=request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    
    chapter_id=data.get('chapter_id')
    if not chapter_id:
        return {'message': 'Chapter ID is required'}, 400
    
    try:
        chapter_id=uuid.UUID(chapter_id)
    except ValueError:
        return {'message': 'Invalid chapter ID'}, 400
    
    chapter=Chapter.query.get(chapter_id)
    if not chapter:
        return {'message': 'Chapter not found'}, 404
    
    db.session.delete(chapter)
    db.session.commit()
    return {'message': 'Chapter deleted successfully'}, 200


@app.route("/admin_logout", methods=["POST"])
@jwt_required()
def admin_logout():
    return jsonify({"message": "Logout successful"}), 200


@app.route('/admin_search/<query>', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=60)
def admin_search(query):
    token = get_jwt()
    if not token['type'] == 'admin':
        return {'message': 'Now allowed to access this page, login as admin'}, 401
    
    users = User.query.filter(User.user_name.ilike(f"%{query}%")).all()
    subjects = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.quiz_name.ilike(f"%{query}%")).all()
    questions=Question.query.filter(Question.question_statement.ilike(f"%{query}%")).all()
    results = []
    results.extend([{"name": user.user_name, "type": "User"} for user in users])
    results.extend([{"name": subject.subject_name, "type": "Subject"} for subject in subjects])
    results.extend([{"name": quiz.quiz_name, "type": "Quiz"} for quiz in quizzes])
    results.extend([{"name": question.question_statement, "type": "Question"} for question in questions])

    return jsonify(results)




@app.route('/user_search/<query>', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=60)
def user_search(query):
    token = get_jwt()
    if not token['type'] == 'user':
        return {'message': 'Now allowed to access this page, login as user'}, 401
    subjects = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    chapters=Chapter.query.filter(Chapter.chapter_name.ilike(f"%{query}%")).all()
    
    results = []
    for subject in subjects:
        results.append({
            "type": "Subject",
            "name": subject.subject_name,
            "chapters": [{"id": str(chapter.id), "name": chapter.chapter_name} for chapter in subject.chapters]
        })

    for chapter in chapters:
        results.append({
            "type": "Chapter",
            "name": chapter.chapter_name,
            "description": chapter.chapter_description,
            "subject_name": chapter.subject.subject_name,  # Fetch subject name for reference
            "quizzes": [{"id": str(quiz.id), "name": quiz.quiz_name} for quiz in chapter.quizzes]
        })
    
    
    quizzes = Quiz.query.filter(Quiz.quiz_name.ilike(f"%{query}%")).all()
    questions=Question.query.filter(Question.question_statement.ilike(f"%{query}%")).all()

    results.extend([{"name": quiz.quiz_name, "type": "Quiz"} for quiz in quizzes])
    results.extend([{"name": question.question_statement, "type": "Question"} for question in questions])

    return jsonify(results)


