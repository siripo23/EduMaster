#!/usr/bin/env python3
"""
Add more sample questions to database for testing
"""

from app import app
from models import db, Question

def add_sample_questions():
    """Add more sample questions"""
    
    with app.app_context():
        questions = []
        
        # NEET Physics Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Physics',
                chapter='Mechanics',
                topic='Motion',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Physics Question {i}: What is the SI unit of force?',
                option_a='Newton',
                option_b='Joule',
                option_c='Watt',
                option_d='Pascal',
                correct_answer='A',
                explanation='The SI unit of force is Newton (N)',
                stream='NEET'
            ))
        
        # NEET Chemistry Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Chemistry',
                chapter='Organic Chemistry',
                topic='Hydrocarbons',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Chemistry Question {i}: What is the molecular formula of methane?',
                option_a='CH4',
                option_b='C2H6',
                option_c='C3H8',
                option_d='C4H10',
                correct_answer='A',
                explanation='Methane has the molecular formula CH4',
                stream='NEET'
            ))
        
        # NEET Biology Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Biology',
                chapter='Cell Biology',
                topic='Cell Structure',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Biology Question {i}: What is the powerhouse of the cell?',
                option_a='Mitochondria',
                option_b='Nucleus',
                option_c='Ribosome',
                option_d='Golgi apparatus',
                correct_answer='A',
                explanation='Mitochondria is known as the powerhouse of the cell',
                stream='NEET'
            ))
        
        # JEE Physics Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Physics',
                chapter='Mechanics',
                topic='Motion',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Physics Question {i}: What is the SI unit of energy?',
                option_a='Joule',
                option_b='Newton',
                option_c='Watt',
                option_d='Pascal',
                correct_answer='A',
                explanation='The SI unit of energy is Joule (J)',
                stream='JEE'
            ))
        
        # JEE Chemistry Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Chemistry',
                chapter='Physical Chemistry',
                topic='Thermodynamics',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Chemistry Question {i}: What is the value of Avogadro number?',
                option_a='6.022 × 10²³',
                option_b='6.022 × 10²²',
                option_c='6.022 × 10²⁴',
                option_d='6.022 × 10²¹',
                correct_answer='A',
                explanation='Avogadro number is 6.022 × 10²³',
                stream='JEE'
            ))
        
        # JEE Mathematics Questions (15 more)
        for i in range(1, 16):
            questions.append(Question(
                subject='Mathematics',
                chapter='Algebra',
                topic='Quadratic Equations',
                difficulty=['Easy', 'Medium', 'Hard'][i % 3],
                question_text=f'Sample Mathematics Question {i}: What is the value of π (pi)?',
                option_a='3.14159',
                option_b='2.71828',
                option_c='1.41421',
                option_d='1.73205',
                correct_answer='A',
                explanation='The value of π is approximately 3.14159',
                stream='JEE'
            ))
        
        # Add all questions
        for q in questions:
            db.session.add(q)
        
        db.session.commit()
        
        print(f"✅ Added {len(questions)} sample questions")
        print(f"📊 Total questions in database: {Question.query.count()}")
        
        # Show breakdown
        neet_count = Question.query.filter_by(stream='NEET').count()
        jee_count = Question.query.filter_by(stream='JEE').count()
        
        print(f"\n📚 Questions by Stream:")
        print(f"   NEET: {neet_count} questions")
        print(f"   JEE: {jee_count} questions")

if __name__ == '__main__':
    add_sample_questions()
