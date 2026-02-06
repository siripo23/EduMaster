from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Question, TestAttempt, Resource
from ai_engine import AdaptiveTestEngine
from config import config
import os
from datetime import datetime

# Create Flask app with configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app = Flask(__name__)
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize AI engine
ai_engine = AdaptiveTestEngine()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        class_level = request.form['class_level']
        stream = request.form['stream']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            class_level=class_level,
            stream=stream
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('initial_test'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent test attempts
    recent_tests = TestAttempt.query.filter_by(user_id=current_user.id)\
                                  .order_by(TestAttempt.created_at.desc())\
                                  .limit(5).all()
    
    # Get performance statistics
    total_tests = TestAttempt.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         user=current_user, 
                         recent_tests=recent_tests,
                         total_tests=total_tests)

@app.route('/initial_test')
@login_required
def initial_test():
    # Check if user has already taken initial test
    if current_user.initial_test_score > 0:
        return redirect(url_for('dashboard'))
    
    # Generate initial test questions
    questions = ai_engine.generate_initial_test(current_user.stream)
    session['test_questions'] = [q.id for q in questions]
    session['test_type'] = 'initial'
    session['test_start_time'] = datetime.now().isoformat()
    
    return render_template('test.html', 
                         questions=questions, 
                         test_type='Initial Level Test')

@app.route('/adaptive_test')
@login_required
def adaptive_test():
    # Generate adaptive test based on user's profile
    questions = ai_engine.generate_adaptive_test(current_user)
    session['test_questions'] = [q.id for q in questions]
    session['test_type'] = 'adaptive'
    session['test_start_time'] = datetime.now().isoformat()
    
    return render_template('test.html', 
                         questions=questions, 
                         test_type='Adaptive Test')

@app.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    if 'test_questions' not in session:
        return redirect(url_for('dashboard'))
    
    # Get test data from session
    question_ids = session['test_questions']
    test_type = session['test_type']
    start_time = datetime.fromisoformat(session['test_start_time'])
    
    # Calculate time taken
    time_taken = int((datetime.now() - start_time).total_seconds() / 60)
    
    # Get answers from form
    answers = {}
    for q_id in question_ids:
        answer = request.form.get(f'question_{q_id}')
        if answer:
            answers[str(q_id)] = answer
    
    # Calculate score
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    correct_answers = 0
    
    for question in questions:
        if answers.get(str(question.id)) == question.correct_answer:
            correct_answers += 1
    
    # Create test attempt record
    test_attempt = TestAttempt(
        user_id=current_user.id,
        test_type=test_type,
        score=correct_answers,
        total_questions=len(question_ids),
        time_taken=time_taken
    )
    test_attempt.set_questions_attempted(question_ids)
    test_attempt.set_answers_given(answers)
    
    db.session.add(test_attempt)
    db.session.commit()
    
    # Analyze performance and update user profile
    analysis = ai_engine.analyze_test_performance(current_user, test_attempt)
    db.session.commit()
    
    # Clear session data
    session.pop('test_questions', None)
    session.pop('test_type', None)
    session.pop('test_start_time', None)
    
    return render_template('test_results.html', 
                         test_attempt=test_attempt,
                         analysis=analysis)

@app.route('/resources')
@login_required
def resources():
    # Get resources for user's stream
    textbooks = Resource.query.filter_by(
        stream=current_user.stream,
        resource_type='textbook'
    ).all()
    
    past_papers = Resource.query.filter_by(
        stream=current_user.stream,
        resource_type='past_paper'
    ).order_by(Resource.year.desc()).all()
    
    return render_template('resources.html', 
                         textbooks=textbooks,
                         past_papers=past_papers)

@app.route('/profile')
@login_required
def profile():
    # Get user's performance history
    test_history = TestAttempt.query.filter_by(user_id=current_user.id)\
                                  .order_by(TestAttempt.created_at.desc()).all()
    
    return render_template('profile.html', 
                         user=current_user,
                         test_history=test_history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)