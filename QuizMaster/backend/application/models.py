from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
 


db = SQLAlchemy()
 
class Admin(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_name=db.Column(db.String(50))
    admin_email=db.Column(db.String(50), nullable=False)
    admin_password=db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            'admin_email': self.admin_email,
            #'admin_password': self.admin_password,
            'admin_name': self.admin_name
        }
    def __repr__(self):
        return f"<Admin {self.admin_name}>"

# many to many relationship between user and quiz
user_quiz_association = db.Table(
    'user_quiz_association',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id'), primary_key=True),
    db.Column('quiz_id', UUID(as_uuid=True), db.ForeignKey('quiz.id'), primary_key=True)
)
 

class User(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = db.Column(db.String(120), unique=True)
    user_password = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    user_qualification = db.Column(db.String(80))  
    user_dob = db.Column(db.String(10)) 
    
    last_visited_time = db.Column(db.DateTime, default=datetime.now)  # New field
    reminder_time = db.Column(db.DateTime, nullable=True)  
    quizzes=db.relationship("Quiz", secondary=user_quiz_association,back_populates='users', lazy='dynamic')

    def to_json(self):
        return {
            #'id':self.id,
            'user_email': self.user_email,
            'user_name': self.user_name,
            'user_qualification': self.user_qualification,
            'user_dob': self.user_dob,
            "last_visited_time": str(self.last_visited_time),
        }
    def __repr__(self):
        return f"<User {self.user_name}>"
    


class Subject(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_name = db.Column(db.String(200), nullable=False, unique=True) 
    subject_description = db.Column(db.Text, nullable=True)
    
    def to_json(self):
        return {
            'id':self.id,
            'subject_name': self.subject_name,
            'subject_description': self.subject_description,
            'chapters': [chapter.to_json() for chapter in self.chapters]
        }

    def __repr__(self):
        return f"<Course {self.subject_name}>"



class Chapter(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_name = db.Column(db.String(200), nullable=False, unique=True)
    chapter_description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subject.id'), nullable=False)

    subject=db.relationship('Subject', backref=db.backref('chapters', cascade='all, delete-orphan'))
    # Deletes subject and its child chapter both.    
    def to_json(self):
        return {
            'id': str(self.id),
            'chapter_name': self.chapter_name,
            'chapter_description': self.chapter_description,
            'subject_id': str(self.subject_id)
        }
    def __repr__(self):
        return f"<Module {self.chapter_name}>"


class Quiz(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = db.Column(UUID(as_uuid=True), db.ForeignKey('chapter.id'), nullable=True)
    quiz_name = db.Column(db.String(200), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration=db.Column(db.Integer, nullable=False)
    
    users=db.relationship("User", secondary=user_quiz_association,back_populates='quizzes', lazy='dynamic')
    chapter=db.relationship('Chapter', backref='quizzes')
    questions=db.relationship("Question", backref='quiz', lazy=True)

    def to_json(self):
        return {
            'id':str(self.id),
            'quiz_name': self.quiz_name,
            'date_of_quiz': self.date_of_quiz.isoformat(),
            'time_duration': self.time_duration,
            'chapter_id': str(self.chapter_id),
            'questions': [ q.to_json() for q in self.questions ]
        }
    def __repr__(self):
        return f"<Quiz {self.quiz_name}>"
    

class Question(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False, unique=True)
    option1 = db.Column(db.String(200), nullable=True)
    option2 = db.Column(db.String(200), nullable=True)
    option3 = db.Column(db.String(200), nullable=True)
    option4 = db.Column(db.String(200), nullable=True)
    correct_option = db.Column(db.String(200), nullable=False)

    def to_json(self):
        return {
            'id':self.id,
            'quiz_id': str(self.quiz_id),
            'question_statement': self.question_statement,
            'option1': self.option1,
            'option2': self.option2,
            'option3': self.option3,
            'option4': self.option4,
            'correct_option': self.correct_option
        }
    def __repr__(self):
        return f"<Question {self.question_statement}>"


class Score(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz.id'), nullable=False)
    time_of_attempt = db.Column(db.DateTime, nullable=False) 
    total_score = db.Column(db.Integer, nullable=False)

    quiz=db.relationship("Quiz", backref='scores', lazy=True)

    def to_json(self):
        return {
            'id':self.id,
            'user_id': str(self.user_id),
            'quiz_id': str(self.quiz_id),
            'quiz_name':self.quiz.quiz_name,
            'time_of_attempt': self.time_of_attempt.isoformat(),
            'total_score': self.total_score
        }

    def __repr__(self):
        return f"<Score {self.total_score}>"



