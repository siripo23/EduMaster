# Enhanced Test System Implementation Guide

## Features Implemented

### 1. Test System Enhancements
- ✅ **Negative Marking**: +4 for correct, -1 for wrong answers
- ✅ **Test Start Page**: Instructions and agreement before starting
- ✅ **Timer**: Countdown timer with auto-submit on expiry
- ✅ **Fullscreen Mode**: Mandatory fullscreen with exit detection
- ✅ **Tab Switch Detection**: Automatic submission on tab switching
- ✅ **AI Tool Detection**: Basic detection of developer tools and copy/paste
- ✅ **Question Navigator**: Visual palette showing answered/unanswered questions
- ✅ **Mark for Review**: Flag questions for later review
- ✅ **Auto-save**: Progress saved every 30 seconds

### 2. Files Created

#### Templates:
- `templates/test_start.html` - Pre-test instructions page
- `templates/test_enhanced.html` - Enhanced test interface
- `static/css/test_enhanced.css` - Test styling
- `static/js/test_enhanced.js` - Test security and functionality

### 3. Required App.py Changes

Add these routes to `app.py`:

```python
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
        total_questions = 180  # NEET/JEE full paper
        duration = 180
    else:
        total_questions = 30
        duration = 45
    
    return render_template('test_start.html',
                         test_type=test_type.replace('_', ' ').title(),
                         total_questions=total_questions,
                         duration=duration)

@app.route('/test/take/<test_type>')
@login_required
def take_test(test_type):
    """Start the actual test"""
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
        subject = test_type.replace('subject_', '').title()
        questions = ai_engine.generate_subject_test(current_user.stream, subject)
        duration = 45
    else:
        questions = ai_engine.generate_adaptive_test(current_user)
        duration = 60
    
    # Store in session
    session['test_questions'] = [q.id for q in questions]
    session['test_type'] = test_type
    session['test_start_time'] = datetime.now().isoformat()
    session['test_duration'] = duration
    
    return render_template('test_enhanced.html',
                         questions=questions,
                         test_type=test_type.replace('_', ' ').title(),
                         duration=duration)

# Update submit_test to include negative marking
@app.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    if 'test_questions' not in session:
        return redirect(url_for('dashboard'))
    
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
    
    # Calculate score with negative marking
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
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
    db.session.commit()
    
    # Analyze performance
    analysis = ai_engine.analyze_test_performance(current_user, test_attempt)
    db.session.commit()
    
    # Clear session
    session.pop('test_questions', None)
    session.pop('test_type', None)
    session.pop('test_start_time', None)
    session.pop('test_duration', None)
    
    return render_template('test_results.html',
                         test_attempt=test_attempt,
                         analysis=analysis,
                         correct=correct_answers,
                         wrong=wrong_answers,
                         unattempted=unattempted)
```

### 4. AI Engine Enhancements

Add these methods to `ai_engine.py`:

```python
def generate_full_paper(self, stream, num_questions=180):
    """Generate a full NEET/JEE paper"""
    subjects = self._get_subjects_for_stream(stream)
    
    if stream == 'NEET':
        # NEET: 45 Physics, 45 Chemistry, 90 Biology
        distribution = {'Physics': 45, 'Chemistry': 45, 'Biology': 90}
    else:
        # JEE: 60 Physics, 60 Chemistry, 60 Mathematics
        distribution = {'Physics': 60, 'Chemistry': 60, 'Mathematics': 60}
    
    selected_questions = []
    
    for subject, count in distribution.items():
        questions = Question.query.filter_by(
            subject=subject,
            stream=stream
        ).order_by(Question.id.desc()).limit(count * 2).all()
        
        selected_questions.extend(random.sample(questions, min(count, len(questions))))
    
    random.shuffle(selected_questions)
    return selected_questions

def generate_subject_test(self, stream, subject, num_questions=30):
    """Generate subject-specific test"""
    questions = Question.query.filter_by(
        subject=subject,
        stream=stream
    ).order_by(Question.id.desc()).limit(num_questions * 2).all()
    
    selected = random.sample(questions, min(num_questions, len(questions)))
    random.shuffle(selected)
    return selected
```

### 5. Resources System Enhancement

For collecting data from various sources, you'll need to:

1. **Create a data collection script** (`scripts/collect_resources.py`):
   - Scrape NTA official website for past papers
   - Download NCERT textbooks (ensure legal compliance)
   - Collect mock tests from government sources
   - Store in `static/resources/` folder

2. **Update database** with actual file paths

3. **Implement download tracking** in resources route

### 6. Test Types to Add

Update dashboard to show these test options:

```html
<!-- In dashboard.html, add test type selection -->
<div class="test-types">
    <a href="{{ url_for('test_start', test_type='full_paper') }}" class="test-type-card">
        <i class="fas fa-file-alt"></i>
        <h5>Full Paper</h5>
        <p>Complete NEET/JEE mock test</p>
    </a>
    
    <a href="{{ url_for('test_start', test_type='subject_Physics') }}" class="test-type-card">
        <i class="fas fa-atom"></i>
        <h5>Physics Test</h5>
        <p>Subject-specific practice</p>
    </a>
    
    <a href="{{ url_for('test_start', test_type='subject_Chemistry') }}" class="test-type-card">
        <i class="fas fa-flask"></i>
        <h5>Chemistry Test</h5>
        <p>Subject-specific practice</p>
    </a>
    
    <!-- Add more subject tests -->
</div>
```

### 7. Security Notes

The implemented security features include:
- Fullscreen enforcement
- Tab switch detection (1 warning, then auto-submit)
- Copy/paste prevention
- Developer tools detection (basic)
- Timer with auto-submit
- Progress auto-save

**Limitations:**
- Cannot detect all AI tools (ChatGPT in another device, etc.)
- Advanced users can bypass some restrictions
- Consider server-side monitoring for production

### 8. Next Steps

1. Update `app.py` with new routes
2. Update `ai_engine.py` with new methods
3. Test the new test system
4. Collect and add actual resource files
5. Update dashboard with test type selection
6. Add analytics for test performance

### 9. Database Migration

If needed, update the TestAttempt model to store more detailed scores:

```python
# In models.py, the subject_scores field already exists
# Just ensure it stores the detailed breakdown
```

## Usage

1. User clicks "Take Test" from dashboard
2. Redirected to `/test/start/<test_type>` - shows instructions
3. User agrees and clicks "Start Test"
4. Enters fullscreen mode
5. Redirected to `/test/take/<test_type>` - actual test
6. Security monitoring active
7. On submit or time expiry, redirected to results

## Testing

Test with: `test@test.com` / `test123`

Try:
- Switching tabs (should trigger warning/submission)
- Exiting fullscreen (should trigger submission)
- Timer expiry (should auto-submit)
- Negative marking calculation
