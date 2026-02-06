#!/usr/bin/env python3
"""
Database initialization script for NEET/JEE Learning App
Creates tables and populates with sample questions and resources
"""

from app import app
from models import db, Question, Resource
import json

def create_sample_questions():
    """Create sample questions for both NEET and JEE streams"""
    
    # NEET Physics Questions
    neet_physics_questions = [
        {
            'subject': 'Physics',
            'chapter': 'Mechanics',
            'topic': 'Laws of Motion',
            'difficulty': 'Easy',
            'question_text': 'What is the SI unit of force?',
            'option_a': 'Newton',
            'option_b': 'Joule',
            'option_c': 'Watt',
            'option_d': 'Pascal',
            'correct_answer': 'A',
            'explanation': 'The SI unit of force is Newton (N), named after Sir Isaac Newton.',
            'stream': 'NEET'
        },
        {
            'subject': 'Physics',
            'chapter': 'Thermodynamics',
            'topic': 'Heat Transfer',
            'difficulty': 'Medium',
            'question_text': 'Which of the following is NOT a method of heat transfer?',
            'option_a': 'Conduction',
            'option_b': 'Convection',
            'option_c': 'Radiation',
            'option_d': 'Sublimation',
            'correct_answer': 'D',
            'explanation': 'Sublimation is a phase change, not a method of heat transfer.',
            'stream': 'NEET'
        },
        {
            'subject': 'Physics',
            'chapter': 'Optics',
            'topic': 'Reflection',
            'difficulty': 'Hard',
            'question_text': 'A concave mirror has a focal length of 20 cm. An object is placed 30 cm from the mirror. What is the image distance?',
            'option_a': '60 cm',
            'option_b': '12 cm',
            'option_c': '15 cm',
            'option_d': '10 cm',
            'correct_answer': 'A',
            'explanation': 'Using mirror formula: 1/f = 1/u + 1/v, where f=20, u=30, solving gives v=60 cm.',
            'stream': 'NEET'
        }
    ]
    
    # NEET Chemistry Questions
    neet_chemistry_questions = [
        {
            'subject': 'Chemistry',
            'chapter': 'Atomic Structure',
            'topic': 'Electronic Configuration',
            'difficulty': 'Easy',
            'question_text': 'What is the maximum number of electrons in the M shell?',
            'option_a': '8',
            'option_b': '18',
            'option_c': '32',
            'option_d': '2',
            'correct_answer': 'B',
            'explanation': 'The M shell (n=3) can hold a maximum of 2n² = 2(3)² = 18 electrons.',
            'stream': 'NEET'
        },
        {
            'subject': 'Chemistry',
            'chapter': 'Organic Chemistry',
            'topic': 'Hydrocarbons',
            'difficulty': 'Medium',
            'question_text': 'Which of the following is an alkyne?',
            'option_a': 'C₂H₆',
            'option_b': 'C₂H₄',
            'option_c': 'C₂H₂',
            'option_d': 'C₆H₆',
            'correct_answer': 'C',
            'explanation': 'C₂H₂ (acetylene) is an alkyne with a triple bond between carbon atoms.',
            'stream': 'NEET'
        }
    ]
    
    # NEET Biology Questions
    neet_biology_questions = [
        {
            'subject': 'Biology',
            'chapter': 'Cell Biology',
            'topic': 'Cell Organelles',
            'difficulty': 'Easy',
            'question_text': 'Which organelle is known as the powerhouse of the cell?',
            'option_a': 'Nucleus',
            'option_b': 'Mitochondria',
            'option_c': 'Ribosome',
            'option_d': 'Golgi apparatus',
            'correct_answer': 'B',
            'explanation': 'Mitochondria produce ATP through cellular respiration, earning the title "powerhouse of the cell".',
            'stream': 'NEET'
        },
        {
            'subject': 'Biology',
            'chapter': 'Genetics',
            'topic': 'Mendel\'s Laws',
            'difficulty': 'Medium',
            'question_text': 'In a monohybrid cross between two heterozygous parents (Aa × Aa), what is the phenotypic ratio?',
            'option_a': '1:1',
            'option_b': '1:2:1',
            'option_c': '3:1',
            'option_d': '9:3:3:1',
            'correct_answer': 'C',
            'explanation': 'In a monohybrid cross Aa × Aa, the phenotypic ratio is 3:1 (dominant:recessive).',
            'stream': 'NEET'
        }
    ]
    
    # JEE Questions (Physics, Chemistry, Mathematics)
    jee_physics_questions = [
        {
            'subject': 'Physics',
            'chapter': 'Mechanics',
            'topic': 'Kinematics',
            'difficulty': 'Medium',
            'question_text': 'A ball is thrown vertically upward with initial velocity 20 m/s. What is the maximum height reached? (g = 10 m/s²)',
            'option_a': '10 m',
            'option_b': '20 m',
            'option_c': '40 m',
            'option_d': '30 m',
            'correct_answer': 'B',
            'explanation': 'Using v² = u² - 2gh, at maximum height v=0, so h = u²/2g = 400/20 = 20 m.',
            'stream': 'JEE'
        }
    ]
    
    jee_chemistry_questions = [
        {
            'subject': 'Chemistry',
            'chapter': 'Physical Chemistry',
            'topic': 'Chemical Equilibrium',
            'difficulty': 'Hard',
            'question_text': 'For the reaction N₂ + 3H₂ ⇌ 2NH₃, if Kc = 4, what is Kp at 500K? (R = 0.082)',
            'option_a': '4 × (0.082 × 500)²',
            'option_b': '4 / (0.082 × 500)²',
            'option_c': '4 × (0.082 × 500)',
            'option_d': '4',
            'correct_answer': 'B',
            'explanation': 'Kp = Kc(RT)^Δn, where Δn = 2-4 = -2, so Kp = Kc/(RT)².',
            'stream': 'JEE'
        }
    ]
    
    jee_math_questions = [
        {
            'subject': 'Mathematics',
            'chapter': 'Calculus',
            'topic': 'Differentiation',
            'difficulty': 'Easy',
            'question_text': 'What is the derivative of x³?',
            'option_a': '3x²',
            'option_b': 'x²',
            'option_c': '3x',
            'option_d': 'x³/3',
            'correct_answer': 'A',
            'explanation': 'Using the power rule: d/dx(xⁿ) = nxⁿ⁻¹, so d/dx(x³) = 3x².',
            'stream': 'JEE'
        },
        {
            'subject': 'Mathematics',
            'chapter': 'Algebra',
            'topic': 'Quadratic Equations',
            'difficulty': 'Medium',
            'question_text': 'What are the roots of the equation x² - 5x + 6 = 0?',
            'option_a': '2, 3',
            'option_b': '1, 6',
            'option_c': '-2, -3',
            'option_d': '5, 1',
            'correct_answer': 'A',
            'explanation': 'Factoring: (x-2)(x-3) = 0, so x = 2 or x = 3.',
            'stream': 'JEE'
        }
    ]
    
    # Combine all questions
    all_questions = (neet_physics_questions + neet_chemistry_questions + 
                    neet_biology_questions + jee_physics_questions + 
                    jee_chemistry_questions + jee_math_questions)
    
    # Add questions to database
    for q_data in all_questions:
        question = Question(**q_data)
        db.session.add(question)
    
    # Create additional questions for better test variety
    create_additional_questions()

def create_additional_questions():
    """Create more questions for comprehensive testing"""
    
    # Additional NEET questions
    additional_neet = [
        # More Physics
        {
            'subject': 'Physics', 'chapter': 'Electricity', 'topic': 'Current Electricity',
            'difficulty': 'Easy', 'stream': 'NEET',
            'question_text': 'What is the unit of electric current?',
            'option_a': 'Volt', 'option_b': 'Ampere', 'option_c': 'Ohm', 'option_d': 'Watt',
            'correct_answer': 'B', 'explanation': 'The SI unit of electric current is Ampere (A).'
        },
        {
            'subject': 'Physics', 'chapter': 'Waves', 'topic': 'Sound Waves',
            'difficulty': 'Medium', 'stream': 'NEET',
            'question_text': 'The speed of sound in air at 20°C is approximately:',
            'option_a': '330 m/s', 'option_b': '340 m/s', 'option_c': '350 m/s', 'option_d': '360 m/s',
            'correct_answer': 'B', 'explanation': 'At 20°C, sound travels at approximately 340 m/s in air.'
        },
        # More Chemistry
        {
            'subject': 'Chemistry', 'chapter': 'Periodic Table', 'topic': 'Periodic Trends',
            'difficulty': 'Easy', 'stream': 'NEET',
            'question_text': 'Which element has the highest electronegativity?',
            'option_a': 'Oxygen', 'option_b': 'Nitrogen', 'option_c': 'Fluorine', 'option_d': 'Chlorine',
            'correct_answer': 'C', 'explanation': 'Fluorine has the highest electronegativity value of 4.0.'
        },
        # More Biology
        {
            'subject': 'Biology', 'chapter': 'Ecology', 'topic': 'Ecosystem',
            'difficulty': 'Medium', 'stream': 'NEET',
            'question_text': 'Which of the following is a primary consumer?',
            'option_a': 'Lion', 'option_b': 'Rabbit', 'option_c': 'Eagle', 'option_d': 'Bacteria',
            'correct_answer': 'B', 'explanation': 'Rabbit is a herbivore and thus a primary consumer in the food chain.'
        }
    ]
    
    # Additional JEE questions
    additional_jee = [
        # More Mathematics
        {
            'subject': 'Mathematics', 'chapter': 'Trigonometry', 'topic': 'Trigonometric Ratios',
            'difficulty': 'Easy', 'stream': 'JEE',
            'question_text': 'What is the value of sin(90°)?',
            'option_a': '0', 'option_b': '1', 'option_c': '1/2', 'option_d': '√3/2',
            'correct_answer': 'B', 'explanation': 'sin(90°) = 1'
        },
        {
            'subject': 'Mathematics', 'chapter': 'Coordinate Geometry', 'topic': 'Straight Lines',
            'difficulty': 'Medium', 'stream': 'JEE',
            'question_text': 'What is the slope of the line passing through points (1,2) and (3,6)?',
            'option_a': '1', 'option_b': '2', 'option_c': '3', 'option_d': '4',
            'correct_answer': 'B', 'explanation': 'Slope = (y₂-y₁)/(x₂-x₁) = (6-2)/(3-1) = 4/2 = 2'
        }
    ]
    
    all_additional = additional_neet + additional_jee
    
    for q_data in all_additional:
        question = Question(**q_data)
        db.session.add(question)

def create_sample_resources():
    """Create sample resources (textbooks and past papers)"""
    
    resources = [
        # NEET Textbooks
        {
            'title': 'NCERT Physics Class 11',
            'resource_type': 'textbook',
            'subject': 'Physics',
            'file_path': '/static/resources/ncert_physics_11.pdf',
            'stream': 'NEET'
        },
        {
            'title': 'NCERT Physics Class 12',
            'resource_type': 'textbook',
            'subject': 'Physics',
            'file_path': '/static/resources/ncert_physics_12.pdf',
            'stream': 'NEET'
        },
        {
            'title': 'NCERT Chemistry Class 11',
            'resource_type': 'textbook',
            'subject': 'Chemistry',
            'file_path': '/static/resources/ncert_chemistry_11.pdf',
            'stream': 'NEET'
        },
        {
            'title': 'NCERT Biology Class 11',
            'resource_type': 'textbook',
            'subject': 'Biology',
            'file_path': '/static/resources/ncert_biology_11.pdf',
            'stream': 'NEET'
        },
        
        # JEE Textbooks
        {
            'title': 'NCERT Mathematics Class 11',
            'resource_type': 'textbook',
            'subject': 'Mathematics',
            'file_path': '/static/resources/ncert_math_11.pdf',
            'stream': 'JEE'
        },
        {
            'title': 'NCERT Mathematics Class 12',
            'resource_type': 'textbook',
            'subject': 'Mathematics',
            'file_path': '/static/resources/ncert_math_12.pdf',
            'stream': 'JEE'
        },
        
        # Past Papers
        {
            'title': 'NEET 2023 Question Paper',
            'resource_type': 'past_paper',
            'subject': 'All Subjects',
            'file_path': '/static/resources/neet_2023.pdf',
            'stream': 'NEET',
            'year': 2023
        },
        {
            'title': 'NEET 2022 Question Paper',
            'resource_type': 'past_paper',
            'subject': 'All Subjects',
            'file_path': '/static/resources/neet_2022.pdf',
            'stream': 'NEET',
            'year': 2022
        },
        {
            'title': 'JEE Main 2023 Question Paper',
            'resource_type': 'past_paper',
            'subject': 'All Subjects',
            'file_path': '/static/resources/jee_main_2023.pdf',
            'stream': 'JEE',
            'year': 2023
        },
        {
            'title': 'JEE Advanced 2023 Question Paper',
            'resource_type': 'past_paper',
            'subject': 'All Subjects',
            'file_path': '/static/resources/jee_advanced_2023.pdf',
            'stream': 'JEE',
            'year': 2023
        }
    ]
    
    for resource_data in resources:
        resource = Resource(**resource_data)
        db.session.add(resource)

def main():
    """Initialize database with tables and sample data"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Adding sample questions...")
        create_sample_questions()
        
        print("Adding sample resources...")
        create_sample_resources()
        
        print("Committing changes...")
        db.session.commit()
        
        # Print statistics
        question_count = Question.query.count()
        resource_count = Resource.query.count()
        
        print(f"\nDatabase initialized successfully!")
        print(f"Total questions: {question_count}")
        print(f"Total resources: {resource_count}")
        
        # Print breakdown by stream
        neet_questions = Question.query.filter_by(stream='NEET').count()
        jee_questions = Question.query.filter_by(stream='JEE').count()
        
        print(f"\nNEET questions: {neet_questions}")
        print(f"JEE questions: {jee_questions}")
        
        print("\nDatabase is ready for use!")

if __name__ == '__main__':
    main()