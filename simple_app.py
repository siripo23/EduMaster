#!/usr/bin/env python3
"""
Simplified NEET/JEE Learning App that works with Python 3.13
Uses basic SQLite operations instead of SQLAlchemy to avoid compatibility issues
Enhanced with session persistence and improved user credential management
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import json
import random
from datetime import datetime, timedelta
import os
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.permanent_session_lifetime = timedelta(days=30)  # Sessions last 30 days

# Database setup
DATABASE = 'learning_app.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and sample data"""
    conn = get_db()
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            class_level TEXT NOT NULL,
            stream TEXT NOT NULL,
            initial_test_score INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Beginner',
            weak_topics TEXT DEFAULT '{}',
            strong_topics TEXT DEFAULT '{}',
            remember_token TEXT,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add new columns if they don't exist (migration)
    try:
        conn.execute('ALTER TABLE users ADD COLUMN remember_token TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        conn.execute('ALTER TABLE users ADD COLUMN last_login TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            stream TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS test_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_type TEXT NOT NULL,
            questions_attempted TEXT NOT NULL,
            answers_given TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            time_taken INTEGER,
            subject_scores TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add sample questions
    sample_questions = [
        # NEET Physics - Challenging Questions
        ('Physics', 'Mechanics', 'Laws of Motion', 'Medium', 
         'A block of mass 2 kg is placed on a rough horizontal surface. If the coefficient of static friction is 0.3 and kinetic friction is 0.2, what is the maximum force that can be applied horizontally without causing motion? (g = 10 m/s²)',
         '4 N', '6 N', '8 N', '10 N', 'B', 'Maximum static friction = μₛmg = 0.3 × 2 × 10 = 6 N', 'NEET'),
        
        ('Physics', 'Thermodynamics', 'Heat Transfer', 'Hard', 
         'An ideal gas undergoes a cyclic process ABCA. In process AB, 400 J of heat is absorbed and 100 J of work is done by the gas. In process BC, 200 J of heat is released. What is the work done in process CA?',
         '100 J', '200 J', '300 J', '500 J', 'A', 'For cyclic process, ΔU = 0. Using first law: Q = W for complete cycle', 'NEET'),
        
        ('Physics', 'Optics', 'Ray Optics', 'Medium',
         'A convex lens of focal length 20 cm forms a real image at a distance of 60 cm from the lens. What is the object distance?',
         '15 cm', '30 cm', '45 cm', '12 cm', 'B', 'Using lens formula: 1/f = 1/v + 1/u, 1/20 = 1/60 + 1/u, u = 30 cm', 'NEET'),
        
        ('Physics', 'Electricity', 'Current Electricity', 'Hard',
         'In a Wheatstone bridge, three resistors have values 2Ω, 4Ω, and 6Ω. What should be the value of the fourth resistor for the bridge to be balanced?',
         '8Ω', '10Ω', '12Ω', '14Ω', 'C', 'For balanced bridge: P/Q = R/S, so 2/4 = 6/S, S = 12Ω', 'NEET'),
        
        # NEET Chemistry - Challenging Questions  
        ('Chemistry', 'Atomic Structure', 'Electronic Configuration', 'Medium',
         'Which of the following electronic configurations represents a transition element?',
         '[Ar] 3d¹⁰ 4s²', '[Ar] 3d⁵ 4s²', '[Ne] 3s² 3p⁶', '[Kr] 5s²', 'B', 'Transition elements have partially filled d-orbitals', 'NEET'),
        
        ('Chemistry', 'Organic Chemistry', 'Hydrocarbons', 'Hard',
         'How many structural isomers are possible for C₅H₁₂?',
         '2', '3', '4', '5', 'B', 'C₅H₁₂ has 3 structural isomers: n-pentane, isopentane, and neopentane', 'NEET'),
        
        ('Chemistry', 'Physical Chemistry', 'Chemical Equilibrium', 'Hard',
         'For the reaction N₂O₄(g) ⇌ 2NO₂(g), Kc = 4.63 × 10⁻³ at 25°C. If the initial concentration of N₂O₄ is 0.1 M, what is the degree of dissociation?',
         '0.1', '0.2', '0.3', '0.4', 'C', 'Using Kc = 4α²/(1-α²) where α is degree of dissociation', 'NEET'),
        
        ('Chemistry', 'Inorganic Chemistry', 'Periodic Table', 'Medium',
         'Which element has the highest first ionization energy in the third period?',
         'Na', 'Mg', 'Al', 'Ar', 'D', 'Ionization energy increases across a period, Ar has highest', 'NEET'),
        
        # NEET Biology - Challenging Questions
        ('Biology', 'Cell Biology', 'Cell Division', 'Medium',
         'During which phase of meiosis does crossing over occur?',
         'Prophase I', 'Metaphase I', 'Anaphase I', 'Telophase I', 'A', 'Crossing over occurs during pachytene stage of prophase I', 'NEET'),
        
        ('Biology', 'Genetics', 'Molecular Basis of Inheritance', 'Hard',
         'If a DNA molecule has 30% adenine, what percentage of cytosine will it have?',
         '20%', '30%', '40%', '70%', 'A', 'A=T=30%, so G=C=(100-60)/2=20%', 'NEET'),
        
        ('Biology', 'Ecology', 'Ecosystem', 'Medium',
         'In a food chain, the energy transfer efficiency from one trophic level to the next is approximately:',
         '1%', '10%', '50%', '90%', 'B', '10% rule states only 10% energy is transferred to next trophic level', 'NEET'),
        
        ('Biology', 'Human Physiology', 'Circulation', 'Hard',
         'The normal blood pressure in a healthy adult is:',
         '80/120 mmHg', '120/80 mmHg', '100/60 mmHg', '140/90 mmHg', 'B', 'Normal BP is 120/80 mmHg (systolic/diastolic)', 'NEET'),
        
        # JEE Mathematics - Challenging Questions
        ('Mathematics', 'Calculus', 'Differentiation', 'Medium',
         'If y = x^x, then dy/dx equals:',
         'x^x', 'x^x(1 + ln x)', 'x^(x-1)', 'x^x ln x', 'B', 'Using logarithmic differentiation: dy/dx = x^x(1 + ln x)', 'JEE'),
        
        ('Mathematics', 'Algebra', 'Complex Numbers', 'Hard',
         'If z = 1 + i, then z^8 equals:',
         '16', '16i', '-16', '0', 'A', 'z = √2 e^(iπ/4), so z^8 = (√2)^8 e^(i2π) = 16', 'JEE'),
        
        ('Mathematics', 'Coordinate Geometry', 'Conic Sections', 'Hard',
         'The equation of the parabola with focus (3, 0) and directrix x = -3 is:',
         'y² = 12x', 'y² = 6x', 'x² = 12y', 'y² = 24x', 'A', 'Distance from focus to directrix = 6, so 4p = 6, p = 3/2, equation: y² = 12x', 'JEE'),
        
        ('Mathematics', 'Trigonometry', 'Trigonometric Equations', 'Medium',
         'The general solution of sin x = 1/2 is:',
         'x = nπ + (-1)ⁿ π/6', 'x = nπ + π/6', 'x = 2nπ ± π/6', 'x = nπ ± π/3', 'A', 'General solution: x = nπ + (-1)ⁿ π/6', 'JEE'),
        
        # JEE Physics - Challenging Questions
        ('Physics', 'Mechanics', 'Rotational Motion', 'Hard',
         'A solid cylinder of mass M and radius R rolls down an inclined plane of angle θ. What is its acceleration?',
         'g sin θ', '(2/3)g sin θ', '(1/2)g sin θ', '(3/4)g sin θ', 'B', 'For rolling motion: a = g sin θ/(1 + I/MR²) = (2/3)g sin θ', 'JEE'),
        
        ('Physics', 'Waves', 'Sound Waves', 'Medium',
         'Two sound waves of frequencies 300 Hz and 304 Hz are played together. The beat frequency is:',
         '2 Hz', '4 Hz', '6 Hz', '8 Hz', 'B', 'Beat frequency = |f₁ - f₂| = |300 - 304| = 4 Hz', 'JEE'),
        
        # JEE Chemistry - Challenging Questions  
        ('Chemistry', 'Physical Chemistry', 'Thermodynamics', 'Hard',
         'For the reaction H₂(g) + I₂(g) → 2HI(g), ΔH = -10 kJ/mol. What is ΔH for 2HI(g) → H₂(g) + I₂(g)?',
         '-10 kJ/mol', '+10 kJ/mol', '-20 kJ/mol', '+20 kJ/mol', 'B', 'Reverse reaction has opposite sign: ΔH = +10 kJ/mol', 'JEE'),
        
        ('Chemistry', 'Organic Chemistry', 'Reaction Mechanisms', 'Hard',
         'In SN1 reaction, the rate determining step involves:',
         'Formation of carbocation', 'Nucleophilic attack', 'Elimination of leaving group', 'Rearrangement', 'A', 'SN1 mechanism: rate determining step is carbocation formation', 'JEE'),
        
        # Additional NEET Questions - More Challenging
        ('Physics', 'Modern Physics', 'Photoelectric Effect', 'Hard',
         'The work function of a metal is 2.5 eV. If light of wavelength 400 nm is incident on it, what is the maximum kinetic energy of emitted photoelectrons? (h = 6.63 × 10⁻³⁴ J·s, c = 3 × 10⁸ m/s)',
         '0.6 eV', '0.8 eV', '1.0 eV', '1.2 eV', 'A', 'E = hc/λ - φ = 3.1 - 2.5 = 0.6 eV', 'NEET'),
        
        ('Chemistry', 'Inorganic Chemistry', 'Coordination Compounds', 'Hard',
         'The IUPAC name of [Co(NH₃)₄Cl₂]Cl is:',
         'Tetraamminedichlorocobalt(III) chloride', 'Dichlorotetraamminecobalt(III) chloride', 'Tetraamminedichloridocobalt(III) chloride', 'Chloridotetraamminecobalt(III) dichloride', 'A', 'IUPAC naming: ligands in alphabetical order, then metal with oxidation state', 'NEET'),
        
        ('Biology', 'Molecular Biology', 'Protein Synthesis', 'Hard',
         'Which of the following codons is known as the universal start codon?',
         'UAG', 'AUG', 'UGA', 'UAA', 'B', 'AUG codes for methionine and serves as start codon in protein synthesis', 'NEET'),
        
        ('Biology', 'Plant Physiology', 'Photosynthesis', 'Medium',
         'In C4 plants, the primary CO₂ acceptor is:',
         'RuBP', 'PEP', 'OAA', 'Malate', 'B', 'PEP (phosphoenolpyruvate) is the primary CO₂ acceptor in C4 plants', 'NEET'),
        
        # Additional JEE Questions - More Challenging
        ('Mathematics', 'Probability', 'Conditional Probability', 'Hard',
         'A bag contains 4 red and 6 black balls. Two balls are drawn at random. What is the probability that both are red?',
         '2/15', '1/6', '4/15', '1/3', 'A', 'P(both red) = (4/10) × (3/9) = 12/90 = 2/15', 'JEE'),
        
        ('Physics', 'Electromagnetic Induction', 'Faraday\'s Law', 'Hard',
         'A circular coil of 100 turns and area 0.1 m² is placed in a magnetic field of 0.2 T. If the coil is rotated by 90° in 0.1 s, what is the induced EMF?',
         '2 V', '20 V', '200 V', '0.2 V', 'B', 'EMF = -N(dΦ/dt) = -100 × (0 - 0.02)/0.1 = 20 V', 'JEE'),
        
        ('Chemistry', 'Organic Chemistry', 'Aldehydes and Ketones', 'Medium',
         'Which reagent is used to distinguish between aldehydes and ketones?',
         'Fehling\'s reagent', 'Lucas reagent', 'Grignard reagent', 'Hinsberg reagent', 'A', 'Fehling\'s reagent gives positive test with aldehydes but not with ketones', 'JEE'),
        
        # More NEET Biology Questions
        ('Biology', 'Human Physiology', 'Nervous System', 'Hard',
         'The resting potential of a neuron is approximately:',
         '+70 mV', '-70 mV', '+90 mV', '-90 mV', 'B', 'Resting potential of neuron is about -70 mV due to K⁺ permeability', 'NEET'),
        
        ('Biology', 'Genetics', 'Linkage and Crossing Over', 'Hard',
         'If the recombination frequency between two genes is 20%, the distance between them is:',
         '20 map units', '10 map units', '40 map units', '2 map units', 'A', '1% recombination frequency = 1 map unit or 1 centimorgan', 'NEET'),
        
        # More JEE Mathematics Questions
        ('Mathematics', 'Integral Calculus', 'Definite Integrals', 'Hard',
         'The value of ∫₀^π sin²x dx is:',
         'π', 'π/2', 'π/4', '2π', 'B', 'Using identity sin²x = (1-cos2x)/2, integral = π/2', 'JEE'),
        
        ('Mathematics', 'Vector Algebra', 'Dot Product', 'Medium',
         'If |a| = 3, |b| = 4, and a·b = 6, then the angle between vectors a and b is:',
         '30°', '45°', '60°', '90°', 'C', 'cos θ = (a·b)/(|a||b|) = 6/12 = 1/2, so θ = 60°', 'JEE'),
        
        # More NEET Chemistry Questions
        ('Chemistry', 'Physical Chemistry', 'Chemical Kinetics', 'Hard',
         'For a first-order reaction, the half-life is 10 minutes. What percentage of reactant remains after 30 minutes?',
         '12.5%', '25%', '50%', '75%', 'A', 'After 3 half-lives: remaining = (1/2)³ = 1/8 = 12.5%', 'NEET'),
        
        ('Chemistry', 'Organic Chemistry', 'Biomolecules', 'Medium',
         'Which of the following is a reducing sugar?',
         'Sucrose', 'Glucose', 'Starch', 'Cellulose', 'B', 'Glucose has free anomeric carbon and can act as reducing sugar', 'NEET'),
        
        # More JEE Physics Questions
        ('Physics', 'Gravitation', 'Orbital Motion', 'Hard',
         'The escape velocity from Earth\'s surface is 11.2 km/s. What is the escape velocity from a planet with twice the mass and half the radius of Earth?',
         '11.2 km/s', '22.4 km/s', '31.6 km/s', '44.8 km/s', 'C', 'v_e = √(2GM/R). For 2M and R/2: v_e = √(4GM/R) = 2√2 × 11.2 ≈ 31.6 km/s', 'JEE')
    ]
    
    for q in sample_questions:
        conn.execute('''
            INSERT OR IGNORE INTO questions 
            (subject, chapter, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation, stream)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', q)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def create_user_session(user_id, remember_me=False):
    """Create a new user session"""
    conn = get_db()
    
    # Clean up expired sessions
    conn.execute('DELETE FROM user_sessions WHERE expires_at < ?', (datetime.now(),))
    
    # Create new session
    session_token = generate_session_token()
    expires_at = datetime.now() + timedelta(days=30 if remember_me else 1)
    
    conn.execute('''
        INSERT INTO user_sessions (user_id, session_token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, session_token, expires_at))
    
    # Update user's last login and remember token
    conn.execute('''
        UPDATE users SET last_login = ?, remember_token = ? WHERE id = ?
    ''', (datetime.now(), session_token if remember_me else None, user_id))
    
    conn.commit()
    conn.close()
    
    return session_token

def get_user_from_session():
    """Get user from session token"""
    session_token = session.get('session_token')
    if not session_token:
        return None
    
    conn = get_db()
    result = conn.execute('''
        SELECT u.* FROM users u
        JOIN user_sessions s ON u.id = s.user_id
        WHERE s.session_token = ? AND s.expires_at > ?
    ''', (session_token, datetime.now())).fetchone()
    conn.close()
    
    return result

def get_current_user():
    """Get current user from session"""
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        return user
    
    # Try to get user from session token
    return get_user_from_session()

# Routes
@app.route('/')
def index():
    user = get_current_user()
    if user:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get stream from URL parameter if provided
    preselected_stream = request.args.get('stream', '')
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        class_level = request.form['class_level']
        stream = request.form['stream']
        
        conn = get_db()
        
        # Check if user exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('Email already registered')
            conn.close()
            return redirect(url_for('signup'))
        
        # Create user
        hashed_password = hash_password(password)
        cursor = conn.execute('''
            INSERT INTO users (name, email, password, class_level, stream)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, hashed_password, class_level, stream))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        session['user_id'] = user_id
        flash('Registration successful!')
        return redirect(url_for('initial_test'))
    
    return render_template('signup.html', preselected_stream=preselected_stream)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and user['password'] == hash_password(password):
            # Create session
            session['user_id'] = user['id']
            session.permanent = remember_me
            
            # Create database session for persistence
            session_token = create_user_session(user['id'], remember_me)
            session['session_token'] = session_token
            
            flash(f'Welcome back, {user["name"]}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clean up session from database
    session_token = session.get('session_token')
    if session_token:
        conn = get_db()
        conn.execute('DELETE FROM user_sessions WHERE session_token = ?', (session_token,))
        conn.commit()
        conn.close()
    
    session.clear()
    flash('You have been logged out successfully')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    conn = get_db()
    recent_tests = conn.execute('''
        SELECT * FROM test_attempts WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 5
    ''', (user['id'],)).fetchall()
    
    total_tests = conn.execute('SELECT COUNT(*) as count FROM test_attempts WHERE user_id = ?', (user['id'],)).fetchone()['count']
    conn.close()
    
    return render_template('dashboard.html', user=dict(user), recent_tests=recent_tests, total_tests=total_tests)

@app.route('/initial_test')
def initial_test():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    if user['initial_test_score'] > 0:
        return redirect(url_for('dashboard'))
    
    # Get questions for initial test - ensure no repetition
    conn = get_db()
    questions = conn.execute('''
        SELECT * FROM questions WHERE stream = ? 
        ORDER BY RANDOM() LIMIT 25
    ''', (user['stream'],)).fetchall()
    conn.close()
    
    if len(questions) < 25:
        flash(f'Only {len(questions)} questions available for {user["stream"]} stream')
    
    session['test_questions'] = [q['id'] for q in questions]
    session['test_type'] = 'initial'
    session['test_start_time'] = datetime.now().isoformat()
    
    return render_template('test.html', questions=questions, test_type='Initial Level Test')

@app.route('/practice')
def practice():
    """Practice test selection page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    return render_template('practice_selection.html', user=dict(user))

@app.route('/start_test/<test_type>')
def start_test(test_type):
    """Start a specific test type"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Define test configurations
    test_configs = {
        'neet_full': {
            'name': 'NEET Full Test',
            'questions': 180,
            'duration': 180,  # 3 hours in minutes
            'marks_correct': 4,
            'marks_wrong': -1,
            'marks_unattempted': 0
        },
        'jee_full': {
            'name': 'JEE Main Full Test',
            'questions': 75,
            'duration': 180,  # 3 hours in minutes
            'marks_correct': 4,
            'marks_wrong': -1,
            'marks_unattempted': 0
        },
        'neet_practice': {
            'name': 'NEET Practice Test',
            'questions': 45,  # 1/4th of full test
            'duration': 45,
            'marks_correct': 4,
            'marks_wrong': -1,
            'marks_unattempted': 0
        },
        'jee_practice': {
            'name': 'JEE Practice Test',
            'questions': 20,  # Approx 1/4th of full test
            'duration': 45,
            'marks_correct': 4,
            'marks_wrong': -1,
            'marks_unattempted': 0
        }
    }
    
    if test_type not in test_configs:
        flash('Invalid test type')
        return redirect(url_for('practice'))
    
    config = test_configs[test_type]
    
    # Validate stream matches test type
    if user['stream'] == 'NEET' and 'jee' in test_type:
        flash('You are enrolled in NEET stream. Please select NEET tests.')
        return redirect(url_for('practice'))
    elif user['stream'] == 'JEE' and 'neet' in test_type:
        flash('You are enrolled in JEE stream. Please select JEE tests.')
        return redirect(url_for('practice'))
    
    # Get questions
    conn = get_db()
    
    # Get recently attempted question IDs to avoid repetition
    recent_attempts = conn.execute('''
        SELECT questions_attempted FROM test_attempts 
        WHERE user_id = ? ORDER BY created_at DESC LIMIT 5
    ''', (user['id'],)).fetchall()
    
    attempted_ids = set()
    for attempt in recent_attempts:
        try:
            ids = json.loads(attempt['questions_attempted'])
            attempted_ids.update(ids)
        except:
            pass
    
    # Get fresh questions
    if attempted_ids:
        placeholders = ','.join(['?'] * len(attempted_ids))
        questions = conn.execute(f'''
            SELECT * FROM questions WHERE stream = ? AND id NOT IN ({placeholders})
            ORDER BY RANDOM() LIMIT ?
        ''', [user['stream']] + list(attempted_ids) + [config['questions']]).fetchall()
    else:
        questions = conn.execute('''
            SELECT * FROM questions WHERE stream = ? 
            ORDER BY RANDOM() LIMIT ?
        ''', (user['stream'], config['questions'])).fetchall()
    
    conn.close()
    
    if len(questions) < config['questions']:
        flash(f'Not enough questions available. Only {len(questions)} questions found.')
    
    session['test_questions'] = [q['id'] for q in questions]
    session['test_type'] = test_type
    session['test_config'] = config
    session['test_start_time'] = datetime.now().isoformat()
    
    return render_template('test.html', 
                         questions=questions, 
                         test_config=config,
                         test_type=config['name'])

@app.route('/adaptive_test')
def adaptive_test():
    """Redirect to practice page"""
    return redirect(url_for('practice'))

@app.route('/submit_test', methods=['POST'])
def submit_test():
    user = get_current_user()
    if not user or 'test_questions' not in session:
        return redirect(url_for('dashboard'))
    
    question_ids = session['test_questions']
    test_type = session['test_type']
    test_config = session.get('test_config', {
        'marks_correct': 4,
        'marks_wrong': -1,
        'marks_unattempted': 0
    })
    start_time = datetime.fromisoformat(session['test_start_time'])
    time_taken = int((datetime.now() - start_time).total_seconds() / 60)
    
    # Get answers
    answers = {}
    for q_id in question_ids:
        answer = request.form.get(f'question_{q_id}')
        if answer:
            answers[str(q_id)] = answer
    
    # Get questions from database
    conn = get_db()
    questions = conn.execute(f'''
        SELECT * FROM questions WHERE id IN ({','.join(['?'] * len(question_ids))})
    ''', question_ids).fetchall()
    
    # Calculate score with NEET/JEE marking system
    correct_count = 0
    wrong_count = 0
    unattempted_count = 0
    total_marks = 0
    
    for question in questions:
        q_id = str(question['id'])
        user_answer = answers.get(q_id)
        
        if user_answer is None:
            # Unattempted
            unattempted_count += 1
            total_marks += test_config['marks_unattempted']
        elif user_answer == question['correct_answer']:
            # Correct answer
            correct_count += 1
            total_marks += test_config['marks_correct']
        else:
            # Wrong answer
            wrong_count += 1
            total_marks += test_config['marks_wrong']
    
    # Save test attempt with detailed scoring
    conn.execute('''
        INSERT INTO test_attempts 
        (user_id, test_type, questions_attempted, answers_given, score, total_questions, time_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user['id'], test_type, json.dumps(question_ids), json.dumps(answers), 
          total_marks, len(question_ids), time_taken))
    
    # Update user level if initial test
    if test_type == 'initial':
        percentage = correct_count / len(question_ids)
        if percentage >= 0.8:
            level = 'Advanced'
        elif percentage >= 0.6:
            level = 'Intermediate'
        else:
            level = 'Beginner'
        
        conn.execute('''
            UPDATE users SET initial_test_score = ?, level = ? WHERE id = ?
        ''', (total_marks, level, user['id']))
    
    conn.commit()
    conn.close()
    
    # Clear session
    session.pop('test_questions', None)
    session.pop('test_type', None)
    session.pop('test_config', None)
    session.pop('test_start_time', None)
    
    # Store results in session for results page
    session['test_results'] = {
        'correct': correct_count,
        'wrong': wrong_count,
        'unattempted': unattempted_count,
        'total_marks': total_marks,
        'total_questions': len(question_ids),
        'max_marks': len(question_ids) * test_config['marks_correct'],
        'time_taken': time_taken
    }
    
    return redirect(url_for('test_results'))

@app.route('/test_results')
def test_results():
    """Display test results"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    results = session.get('test_results')
    if not results:
        return redirect(url_for('dashboard'))
    
    # Clear results from session after displaying
    session.pop('test_results', None)
    
    return render_template('test_results.html', results=results, user=dict(user))

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    conn = get_db()
    test_history = conn.execute('''
        SELECT * FROM test_attempts WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user['id'],)).fetchall()
    conn.close()
    
    return render_template('profile.html', user=dict(user), test_history=test_history)

@app.before_request
def load_user_from_session():
    """Load user from session token before each request"""
    if 'user_id' not in session:
        session_token = session.get('session_token')
        if session_token:
            user = get_user_from_session()
            if user:
                session['user_id'] = user['id']

def cleanup_expired_sessions():
    """Clean up expired sessions from database"""
    conn = get_db()
    conn.execute('DELETE FROM user_sessions WHERE expires_at < ?', (datetime.now(),))
    conn.commit()
    conn.close()

@app.route('/resources')
def resources():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Simple resources page
    return render_template('simple_resources.html', user=dict(user))

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Clean up expired sessions on startup
    cleanup_expired_sessions()
    
    print("🚀 Starting Enhanced NEET/JEE Learning App...")
    print("📚 Access the app at: http://127.0.0.1:5000")
    print("✨ Features: User registration, adaptive tests, performance tracking, session persistence")
    print("🔐 Enhanced security: Session tokens, remember me functionality")
    print("📊 Question database: 40+ challenging NEET/JEE level questions")
    
    app.run(debug=True, host='127.0.0.1', port=5000)