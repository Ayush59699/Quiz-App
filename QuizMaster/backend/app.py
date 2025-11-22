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
from application.models import db
from application.models import *


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =  f"sqlite:///{os.path.join(basedir, 'database_files', 'db.sqlite')}"
app.config['SECRET_KEY'] = 'my-secret-key'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_DEFAULT_TIMEOUT'] = 240 # 4 minutes

app.config['REDIS_URL']='redis://localhost:6379'
app.config['BROKER_URL']='redis://localhost:6379/0'
app.config['result_backend']='redis://localhost:6379/0'
app.config['broker_connection_retry_on_startup']=True
app.config['timezone']='Asia/Kolkata'
app.config['enable_utc']=True



app.app_context().push()

celery=workers.celery
celery.conf.update(broker_url=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'])
celery.Task=workers.ContextTask

app.app_context().push()

cache.init_app(app)
app.app_context().push()    


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user_uuid=uuid.UUID(user_id)
        return db.session.get(Admin, user_uuid) or \
            db.session.get(User, user_uuid)
    except ValueError:
        return None    


with app.app_context(): 
    from application.routes import *
    db.create_all()    
    admin_email = 'admin@gmail.com'
    admin_user = Admin.query.filter_by(admin_email=admin_email).first()
    if not admin_user:
        admin_user = Admin(admin_email=admin_email, admin_password='123456',admin_name='admin')
        db.session.add(admin_user)
        db.session.commit()

    if User.query.count()==0:
        users = [
            User(user_name=f'User {i}', 
                user_email=f'user{i}@gmail.com', 
                user_password='123456', 
                user_qualification='Graduate', 
                user_dob='2000-01-01') 
            for i in range(1, 11)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
    
    
    if Subject.query.count()==0:
        subjects = [
        Subject(subject_name=f"Subject {i}", subject_description=f"Description for Subject {i}") for i in range(1, 11)
        ]
        db.session.bulk_save_objects(subjects)
    
    
    if Chapter.query.count() == 0:
        subject_ids = [sub.id for sub in Subject.query.all()]
        chapters=[]
        
        for i, subject_id in enumerate(subject_ids):
            for j in range(1, 6):  # Each subject gets 5 chapters
                chapters.append(Chapter(
                    id=uuid.uuid4(),
                    chapter_name=f"Chapter {i * 5 + j}",
                    chapter_description=f"Description for Chapter {i * 5 + j}",
                    subject_id=subject_id
                ))    
        db.session.bulk_save_objects(chapters)
    
    if Quiz.query.count() == 0:
        chapter_ids = [ch.id for ch in Chapter.query.all()]
        quizzes = [
            Quiz(quiz_name=f"Quiz {i+1}", date_of_quiz=date.today(), time_duration=30, chapter_id=ch_id)
            for ch_id in chapter_ids for i in range(2)  # 2 quizzes per chapter
        ]
        db.session.bulk_save_objects(quizzes)
    
    if Question.query.count() == 0:
        quiz_ids = [quiz.id for quiz in Quiz.query.all()]
        questions = [
            Question(
                quiz_id=quiz_id,
                question_statement=f"What is the answer to question {i+1}?",
                option1="Option A",
                option2="Option B",
                option3="Option C",
                option4="Option D",
                correct_option="Option A"
            ) 
            for i, quiz_id in enumerate(quiz_ids)
        ]
        db.session.bulk_save_objects(questions)
    
    if Score.query.count() == 0:
        user_ids = [user.id for user in User.query.all()]
        quiz_ids = [quiz.id for quiz in Quiz.query.all()]
    
        scores = [
            Score(
                    user_id=random.choice(user_ids),
                quiz_id=random.choice(quiz_ids),
                time_of_attempt=datetime.now(),
                total_score=random.randint(0, 100)  
            )   
            for _ in range(10)  # Creating 10 score entries
        ]
        db.session.bulk_save_objects(scores)

    db.session.commit()




# routes in application/routes.py




if __name__=='__main__':
    app.run(debug=True, port=8080)





































