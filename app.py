from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Question, TestAttempt, Resource
from ai_engine import AdaptiveTestEngine
from config import config
import os
import secrets
from datetime import datetime, timedelta

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
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
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
            phone=phone,
            password=hashed_password,
            class_level=class_level,
            stream=stream
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('initial_test'))
    
    # Get preselected stream from URL parameter
    preselected_stream = request.args.get('stream', '')
    return render_template('signup.html', preselected_stream=preselected_stream)

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

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        user = None
        if email:
            user = User.query.filter_by(email=email).first()
        elif phone:
            user = User.query.filter_by(phone=phone).first()
        
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            # In production, send email/SMS with reset link
            # For now, we'll just flash the token (for development)
            flash(f'Password reset link has been sent to your {"email" if email else "phone"}. Use this link: /reset_password/{reset_token}')
            return redirect(url_for('login'))
        else:
            flash('No account found with that email or phone number')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        flash('Invalid or expired reset link')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match')
            return render_template('reset_password.html', token=token)
        
        # Update password
        user.password = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        
        flash('Password successfully reset! You can now login with your new password.')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

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
    # Redirect to test start page
    return redirect(url_for('test_start', test_type='initial'))

@app.route('/adaptive_test')
@login_required
def adaptive_test():
    # Redirect to test start page
    return redirect(url_for('test_start', test_type='adaptive'))

@app.route('/test/start/<test_type>')
@login_required
def test_start(test_type):
    """Show test instructions before starting"""
    # Determine test parameters based on type
    if test_type == 'initial':
        total_questions = 25
        duration = 60  # minutes
    elif test_type == 'adaptive':
        total_questions = 30
        duration = 90
    elif test_type == 'full_paper':
        if current_user.stream == 'NEET':
            total_questions = 180
            duration = 180
        else:  # JEE
            total_questions = 180
            duration = 180
    elif test_type.startswith('subject_'):
        total_questions = 30
        duration = 45
    else:
        total_questions = 30
        duration = 60
    
    return render_template('test_start.html',
                         test_type=test_type.replace('_', ' ').title(),
                         total_questions=total_questions,
                         duration=duration)

@app.route('/test/take/<test_type>')
@login_required
def take_test(test_type):
    """Start the actual test"""
    # Clear any previous test session data
    session.pop('test_questions', None)
    session.pop('test_type', None)
    session.pop('test_start_time', None)
    session.pop('test_duration', None)
    
    # Generate questions based on test type
    if test_type == 'initial':
        questions = ai_engine.generate_initial_test(current_user.stream, num_questions=25)
        duration = 60
    elif test_type == 'adaptive':
        questions = ai_engine.generate_adaptive_test(current_user, num_questions=30)
        duration = 90
    elif test_type == 'full_paper':
        questions = ai_engine.generate_full_paper(current_user.stream)
        duration = 180
    elif test_type.startswith('subject_'):
        subject = test_type.replace('subject_', '').replace('_', ' ')
        questions = ai_engine.generate_subject_test(current_user.stream, subject)
        duration = 45
    else:
        questions = ai_engine.generate_adaptive_test(current_user)
        duration = 60
    
    # Check if we have enough questions
    if not questions or len(questions) == 0:
        flash('Not enough questions available in the database. Please contact administrator.')
        return redirect(url_for('dashboard'))
    
    # Store in session
    session['test_questions'] = [q.id for q in questions]
    session['test_type'] = test_type
    session['test_start_time'] = datetime.now().isoformat()
    session['test_duration'] = duration
    
    # Render template with cache control headers
    response = app.make_response(render_template('test_enhanced.html',
                         questions=questions,
                         test_type=test_type.replace('_', ' ').title(),
                         duration=duration))
    
    # Prevent browser caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    if 'test_questions' not in session:
        flash('No active test found. Please start a new test.')
        return redirect(url_for('dashboard'))
    
    try:
        # Get test data from session
        question_ids = session['test_questions']
        test_type = session['test_type']
        start_time = datetime.fromisoformat(session['test_start_time'])
        
        # Validate we have questions
        if not question_ids or len(question_ids) == 0:
            flash('Invalid test data. Please start a new test.')
            return redirect(url_for('dashboard'))
        
        # Calculate time taken
        time_taken = int((datetime.now() - start_time).total_seconds() / 60)
        
        # Get answers from form
        answers = {}
        for q_id in question_ids:
            answer = request.form.get(f'question_{q_id}')
            if answer:
                answers[str(q_id)] = answer
        
        # Calculate score with negative marking
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        
        if not questions or len(questions) == 0:
            flash('Error: Questions not found in database.')
            return redirect(url_for('dashboard'))
        
        correct_answers = 0
        wrong_answers = 0
        unattempted = 0
        
        for question in questions:
            user_answer = answers.get(str(question.id))
            if user_answer:
                if user_answer == question.correct_answer:
                    correct_answers += 1
                else:
                    wrong_answers += 1
            else:
                unattempted += 1
        
        # Calculate final score: +4 for correct, -1 for wrong
        final_score = (correct_answers * 4) - (wrong_answers * 1)
        max_score = len(question_ids) * 4
        
        # Create test attempt record
        test_attempt = TestAttempt(
            user_id=current_user.id,
            test_type=test_type,
            score=final_score,
            total_questions=len(question_ids),
            time_taken=time_taken
        )
        test_attempt.set_questions_attempted(question_ids)
        test_attempt.set_answers_given(answers)
        
        # Store detailed scores
        subject_scores = {
            'correct': correct_answers,
            'wrong': wrong_answers,
            'unattempted': unattempted,
            'final_score': final_score,
            'max_score': max_score
        }
        test_attempt.set_subject_scores(subject_scores)
        
        db.session.add(test_attempt)
        
        # Update user's initial test score if this is initial test
        if test_type == 'initial' and current_user.initial_test_score == 0:
            current_user.initial_test_score = final_score
        
        db.session.commit()
        
        # Analyze performance and update user profile
        analysis = ai_engine.analyze_test_performance(current_user, test_attempt)
        db.session.commit()
        
        # Clear session data
        session.pop('test_questions', None)
        session.pop('test_type', None)
        session.pop('test_start_time', None)
        session.pop('test_duration', None)
        
        return render_template('test_results.html', 
                             test_attempt=test_attempt,
                             analysis=analysis,
                             correct=correct_answers,
                             wrong=wrong_answers,
                             unattempted=unattempted,
                             final_score=final_score,
                             max_score=max_score)
    
    except Exception as e:
        # Log the error and show user-friendly message
        print(f"Error in submit_test: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clear session data
        session.pop('test_questions', None)
        session.pop('test_type', None)
        session.pop('test_start_time', None)
        session.pop('test_duration', None)
        
        flash('An error occurred while submitting your test. Please try again.')
        return redirect(url_for('dashboard'))

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
    try:
        # Get user's performance history
        test_history = TestAttempt.query.filter_by(user_id=current_user.id)\
                                      .order_by(TestAttempt.created_at.desc()).all()
        
        # Debug logging
        print(f"Profile page - User: {current_user.name}, Tests: {len(test_history)}")
        for test in test_history:
            print(f"Test {test.id}: score={test.score}, total={test.total_questions}, max={test.total_questions * 4}")
        
        return render_template('profile.html', 
                             user=current_user,
                             test_history=test_history)
    except Exception as e:
        print(f"Error in profile route: {str(e)}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while loading your profile. Please try again.')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)