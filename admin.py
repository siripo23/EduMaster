#!/usr/bin/env python3
"""
Simple admin interface for managing questions and resources
Run this script to add questions and resources to the database
"""

from app import app
from models import db, Question, Resource
import json

def add_question():
    """Interactive function to add a new question"""
    print("\n=== Add New Question ===")
    
    # Get question details
    stream = input("Stream (NEET/JEE): ").upper()
    if stream not in ['NEET', 'JEE']:
        print("Invalid stream. Please enter NEET or JEE.")
        return
    
    subject = input("Subject: ").title()
    chapter = input("Chapter: ")
    topic = input("Topic: ")
    
    difficulty = input("Difficulty (Easy/Medium/Hard): ").title()
    if difficulty not in ['Easy', 'Medium', 'Hard']:
        print("Invalid difficulty. Please enter Easy, Medium, or Hard.")
        return
    
    question_text = input("Question: ")
    option_a = input("Option A: ")
    option_b = input("Option B: ")
    option_c = input("Option C: ")
    option_d = input("Option D: ")
    
    correct_answer = input("Correct Answer (A/B/C/D): ").upper()
    if correct_answer not in ['A', 'B', 'C', 'D']:
        print("Invalid answer. Please enter A, B, C, or D.")
        return
    
    explanation = input("Explanation (optional): ")
    
    # Create question object
    question = Question(
        subject=subject,
        chapter=chapter,
        topic=topic,
        difficulty=difficulty,
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer,
        explanation=explanation,
        stream=stream
    )
    
    # Add to database
    db.session.add(question)
    db.session.commit()
    
    print(f"Question added successfully! ID: {question.id}")

def add_resource():
    """Interactive function to add a new resource"""
    print("\n=== Add New Resource ===")
    
    title = input("Resource Title: ")
    
    resource_type = input("Type (textbook/past_paper): ").lower()
    if resource_type not in ['textbook', 'past_paper']:
        print("Invalid type. Please enter textbook or past_paper.")
        return
    
    subject = input("Subject: ").title()
    chapter = input("Chapter (optional): ")
    file_path = input("File Path: ")
    
    stream = input("Stream (NEET/JEE): ").upper()
    if stream not in ['NEET', 'JEE']:
        print("Invalid stream. Please enter NEET or JEE.")
        return
    
    year = None
    if resource_type == 'past_paper':
        year_input = input("Year (for past papers): ")
        if year_input:
            try:
                year = int(year_input)
            except ValueError:
                print("Invalid year format.")
                return
    
    # Create resource object
    resource = Resource(
        title=title,
        resource_type=resource_type,
        subject=subject,
        chapter=chapter if chapter else None,
        file_path=file_path,
        stream=stream,
        year=year
    )
    
    # Add to database
    db.session.add(resource)
    db.session.commit()
    
    print(f"Resource added successfully! ID: {resource.id}")

def bulk_add_questions():
    """Add questions from a JSON file"""
    print("\n=== Bulk Add Questions ===")
    
    file_path = input("Enter JSON file path: ")
    
    try:
        with open(file_path, 'r') as f:
            questions_data = json.load(f)
        
        added_count = 0
        for q_data in questions_data:
            question = Question(**q_data)
            db.session.add(question)
            added_count += 1
        
        db.session.commit()
        print(f"Successfully added {added_count} questions!")
        
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    except Exception as e:
        print(f"Error: {e}")

def view_statistics():
    """Display database statistics"""
    print("\n=== Database Statistics ===")
    
    total_questions = Question.query.count()
    total_resources = Resource.query.count()
    
    print(f"Total Questions: {total_questions}")
    print(f"Total Resources: {total_resources}")
    
    # Questions by stream
    neet_questions = Question.query.filter_by(stream='NEET').count()
    jee_questions = Question.query.filter_by(stream='JEE').count()
    
    print(f"\nNEET Questions: {neet_questions}")
    print(f"JEE Questions: {jee_questions}")
    
    # Questions by difficulty
    easy_questions = Question.query.filter_by(difficulty='Easy').count()
    medium_questions = Question.query.filter_by(difficulty='Medium').count()
    hard_questions = Question.query.filter_by(difficulty='Hard').count()
    
    print(f"\nEasy Questions: {easy_questions}")
    print(f"Medium Questions: {medium_questions}")
    print(f"Hard Questions: {hard_questions}")
    
    # Questions by subject
    subjects = db.session.query(Question.subject).distinct().all()
    print(f"\nQuestions by Subject:")
    for subject in subjects:
        count = Question.query.filter_by(subject=subject[0]).count()
        print(f"  {subject[0]}: {count}")

def list_questions():
    """List recent questions"""
    print("\n=== Recent Questions ===")
    
    questions = Question.query.order_by(Question.id.desc()).limit(10).all()
    
    for q in questions:
        print(f"ID: {q.id}")
        print(f"Stream: {q.stream} | Subject: {q.subject} | Difficulty: {q.difficulty}")
        print(f"Question: {q.question_text[:100]}...")
        print(f"Correct Answer: {q.correct_answer}")
        print("-" * 50)

def create_sample_json():
    """Create a sample JSON file for bulk import"""
    sample_questions = [
        {
            "subject": "Physics",
            "chapter": "Mechanics",
            "topic": "Newton's Laws",
            "difficulty": "Easy",
            "question_text": "Newton's first law is also known as?",
            "option_a": "Law of Inertia",
            "option_b": "Law of Acceleration",
            "option_c": "Law of Action-Reaction",
            "option_d": "Law of Gravitation",
            "correct_answer": "A",
            "explanation": "Newton's first law states that an object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force. This is also known as the Law of Inertia.",
            "stream": "NEET"
        },
        {
            "subject": "Mathematics",
            "chapter": "Algebra",
            "topic": "Linear Equations",
            "difficulty": "Medium",
            "question_text": "Solve for x: 2x + 5 = 13",
            "option_a": "x = 3",
            "option_b": "x = 4",
            "option_c": "x = 5",
            "option_d": "x = 6",
            "correct_answer": "B",
            "explanation": "2x + 5 = 13, so 2x = 8, therefore x = 4",
            "stream": "JEE"
        }
    ]
    
    with open('sample_questions.json', 'w') as f:
        json.dump(sample_questions, f, indent=2)
    
    print("Sample JSON file 'sample_questions.json' created!")
    print("You can modify this file and use it for bulk import.")

def main():
    """Main admin interface"""
    with app.app_context():
        while True:
            print("\n" + "="*50)
            print("NEET/JEE Learning App - Admin Interface")
            print("="*50)
            print("1. Add Question")
            print("2. Add Resource")
            print("3. Bulk Add Questions (from JSON)")
            print("4. View Statistics")
            print("5. List Recent Questions")
            print("6. Create Sample JSON")
            print("0. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                add_question()
            elif choice == '2':
                add_resource()
            elif choice == '3':
                bulk_add_questions()
            elif choice == '4':
                view_statistics()
            elif choice == '5':
                list_questions()
            elif choice == '6':
                create_sample_json()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()