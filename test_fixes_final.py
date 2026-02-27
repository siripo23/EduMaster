"""
Test script to verify all fixes
"""
from app import app
from models import db, User, Question
from ai_engine import AdaptiveTestEngine

def test_full_paper_generation():
    """Test that full paper generates 180 questions"""
    with app.app_context():
        engine = AdaptiveTestEngine()
        
        print("\n" + "="*60)
        print("Testing Full Paper Generation")
        print("="*60)
        
        # Test NEET full paper
        print("\n1. NEET Full Paper (should be 180 questions):")
        neet_questions = engine.generate_full_paper('NEET')
        print(f"   Generated: {len(neet_questions)} questions")
        
        # Check for duplicates
        neet_ids = [q.id for q in neet_questions]
        neet_duplicates = len(neet_ids) - len(set(neet_ids))
        print(f"   Duplicates: {neet_duplicates}")
        
        # Test JEE full paper
        print("\n2. JEE Full Paper (should be 180 questions):")
        jee_questions = engine.generate_full_paper('JEE')
        print(f"   Generated: {len(jee_questions)} questions")
        
        # Check for duplicates
        jee_ids = [q.id for q in jee_questions]
        jee_duplicates = len(jee_ids) - len(set(jee_ids))
        print(f"   Duplicates: {jee_duplicates}")

def test_subject_tests():
    """Test that subject tests generate correct subject questions"""
    with app.app_context():
        engine = AdaptiveTestEngine()
        
        print("\n" + "="*60)
        print("Testing Subject-Specific Tests")
        print("="*60)
        
        # Test NEET subjects
        for subject in ['Physics', 'Chemistry', 'Biology']:
            print(f"\n{subject} Test (NEET):")
            questions = engine.generate_subject_test('NEET', subject, num_questions=30)
            print(f"   Generated: {len(questions)} questions")
            
            # Verify all questions are from correct subject
            wrong_subject = [q for q in questions if q.subject != subject]
            if wrong_subject:
                print(f"   ❌ ERROR: {len(wrong_subject)} questions from wrong subject!")
                for q in wrong_subject[:3]:
                    print(f"      - Question {q.id}: {q.subject} (should be {subject})")
            else:
                print(f"   ✓ All questions are from {subject}")
            
            # Check for duplicates
            ids = [q.id for q in questions]
            duplicates = len(ids) - len(set(ids))
            if duplicates > 0:
                print(f"   ❌ ERROR: {duplicates} duplicate questions!")
            else:
                print(f"   ✓ No duplicates")
        
        # Test JEE subjects
        for subject in ['Physics', 'Chemistry', 'Mathematics']:
            print(f"\n{subject} Test (JEE):")
            questions = engine.generate_subject_test('JEE', subject, num_questions=30)
            print(f"   Generated: {len(questions)} questions")
            
            # Verify all questions are from correct subject
            wrong_subject = [q for q in questions if q.subject != subject]
            if wrong_subject:
                print(f"   ❌ ERROR: {len(wrong_subject)} questions from wrong subject!")
                for q in wrong_subject[:3]:
                    print(f"      - Question {q.id}: {q.subject} (should be {subject})")
            else:
                print(f"   ✓ All questions are from {subject}")
            
            # Check for duplicates
            ids = [q.id for q in questions]
            duplicates = len(ids) - len(set(ids))
            if duplicates > 0:
                print(f"   ❌ ERROR: {duplicates} duplicate questions!")
            else:
                print(f"   ✓ No duplicates")

def test_database_stats():
    """Show database statistics"""
    with app.app_context():
        print("\n" + "="*60)
        print("Database Statistics")
        print("="*60)
        
        total = Question.query.count()
        neet = Question.query.filter_by(stream='NEET').count()
        jee = Question.query.filter_by(stream='JEE').count()
        
        print(f"\nTotal questions: {total}")
        print(f"NEET questions: {neet}")
        print(f"JEE questions: {jee}")
        
        # Subject breakdown
        print("\nNEET Subject Breakdown:")
        for subject in ['Physics', 'Chemistry', 'Biology']:
            count = Question.query.filter_by(stream='NEET', subject=subject).count()
            print(f"  {subject}: {count}")
        
        print("\nJEE Subject Breakdown:")
        for subject in ['Physics', 'Chemistry', 'Mathematics']:
            count = Question.query.filter_by(stream='JEE', subject=subject).count()
            print(f"  {subject}: {count}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("RUNNING FINAL FIX VERIFICATION TESTS")
    print("="*60)
    
    test_database_stats()
    test_subject_tests()
    test_full_paper_generation()
    
    print("\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)
    print("\nNOTE: If full paper has less than 180 questions, you need to:")
    print("1. Add OpenAI API key to .env file for AI generation")
    print("2. Or add more questions to the database")
    print("="*60 + "\n")
