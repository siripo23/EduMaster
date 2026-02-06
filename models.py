from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    class_level = db.Column(db.String(10), nullable=False)  # PUC1 or PUC2
    stream = db.Column(db.String(10), nullable=False)  # NEET or JEE
    initial_test_score = db.Column(db.Integer, default=0)
    level = db.Column(db.String(20), default='Beginner')  # Beginner/Intermediate/Advanced
    weak_topics = db.Column(db.Text, default='{}')  # JSON string
    strong_topics = db.Column(db.Text, default='{}')  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_attempts = db.relationship('TestAttempt', backref='user', lazy=True)
    
    def get_weak_topics(self):
        return json.loads(self.weak_topics) if self.weak_topics else {}
    
    def set_weak_topics(self, topics_dict):
        self.weak_topics = json.dumps(topics_dict)
    
    def get_strong_topics(self):
        return json.loads(self.strong_topics) if self.strong_topics else {}
    
    def set_strong_topics(self, topics_dict):
        self.strong_topics = json.dumps(topics_dict)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)  # Physics, Chemistry, Biology, Maths
    chapter = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Medium, Hard
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    explanation = db.Column(db.Text)
    stream = db.Column(db.String(10), nullable=False)  # NEET or JEE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)  # initial, adaptive, chapter
    questions_attempted = db.Column(db.Text, nullable=False)  # JSON string of question IDs
    answers_given = db.Column(db.Text, nullable=False)  # JSON string of answers
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)  # in minutes
    subject_scores = db.Column(db.Text)  # JSON string of subject-wise scores
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_questions_attempted(self):
        return json.loads(self.questions_attempted)
    
    def set_questions_attempted(self, questions_list):
        self.questions_attempted = json.dumps(questions_list)
    
    def get_answers_given(self):
        return json.loads(self.answers_given)
    
    def set_answers_given(self, answers_dict):
        self.answers_given = json.dumps(answers_dict)
    
    def get_subject_scores(self):
        return json.loads(self.subject_scores) if self.subject_scores else {}
    
    def set_subject_scores(self, scores_dict):
        self.subject_scores = json.dumps(scores_dict)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # textbook, past_paper
    subject = db.Column(db.String(50), nullable=False)
    chapter = db.Column(db.String(100))
    file_path = db.Column(db.String(500), nullable=False)
    stream = db.Column(db.String(10), nullable=False)  # NEET or JEE
    year = db.Column(db.Integer)  # for past papers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)