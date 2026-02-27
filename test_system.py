#!/usr/bin/env python3
"""
System Test Script
Tests all major components of the learning app
"""

import os
from app import app
from models import db, Question, User
from ai_engine import AdaptiveTestEngine

def test_database():
    """Test database connectivity and question count"""
    print("\n" + "="*60)
    print("TEST 1: Database")
    print("="*60)
    
    with app.app_context():
        try:
            neet_count = Question.query.filter_by(stream='NEET').count()
            jee_count = Question.query.filter_by(stream='JEE').count()
            total = neet_count + jee_count
            
            print(f"✓ Database connected")
            print(f"✓ NEET questions: {neet_count}")
            print(f"✓ JEE questions: {jee_count}")
            print(f"✓ Total questions: {total}")
            
            if total >= 100:
                print("✓ Sufficient questions in database")
                return True
            else:
                print("⚠ Low question count - AI generation recommended")
                return True
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False

def test_ai_engine():
    """Test AI engine initialization"""
    print("\n" + "="*60)
    print("TEST 2: AI Engine")
    print("="*60)
    
    try:
        engine = AdaptiveTestEngine()
        print("✓ AI Engine initialized")
        
        if engine.ai_generator:
            print("✓ AI Question Generator available")
            if engine.ai_generator.client:
                print("✓ OpenAI client configured")
                print("✓ Ready for AI question generation")
                return True
            else:
                print("⚠ OpenAI API key not configured")
                print("  Add OPENAI_API_KEY to .env file")
                print("  System will use database questions as fallback")
                return True
        else:
            print("⚠ AI Generator not available")
            print("  System will use database questions")
            return True
    except Exception as e:
        print(f"✗ AI Engine error: {e}")
        return False

def test_question_generation():
    """Test question generation"""
    print("\n" + "="*60)
    print("TEST 3: Question Generation")
    print("="*60)
    
    with app.app_context():
        try:
            engine = AdaptiveTestEngine()
            
            # Test adaptive test generation
            print("\nGenerating adaptive test (30 questions)...")
            questions = engine.generate_initial_test('NEET', num_questions=30)
            print(f"✓ Generated {len(questions)} questions")
            
            if len(questions) >= 25:
                print("✓ Sufficient questions generated")
                
                # Check distribution
                subjects = {}
                difficulties = {}
                for q in questions:
                    subjects[q.subject] = subjects.get(q.subject, 0) + 1
                    difficulties[q.difficulty] = difficulties.get(q.difficulty, 0) + 1
                
                print("\nSubject distribution:")
                for subject, count in subjects.items():
                    print(f"  {subject}: {count}")
                
                print("\nDifficulty distribution:")
                for difficulty, count in difficulties.items():
                    print(f"  {difficulty}: {count}")
                
                return True
            else:
                print(f"⚠ Only {len(questions)} questions generated")
                print("  Add more questions to database or configure OpenAI API")
                return False
        except Exception as e:
            print(f"✗ Question generation error: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_theme():
    """Test theme files"""
    print("\n" + "="*60)
    print("TEST 4: Theme Files")
    print("="*60)
    
    try:
        css_path = 'static/css/style.css'
        if os.path.exists(css_path):
            with open(css_path, 'r') as f:
                content = f.read()
                if '--oxford-blue: #002147' in content:
                    print("✓ Oxford Blue theme configured")
                    print("✓ CSS file exists and has correct colors")
                    print("\n⚠ If theme not showing:")
                    print("  1. Clear browser cache (Ctrl + F5)")
                    print("  2. Try different browser")
                    print("  3. Check browser console for errors")
                    return True
                else:
                    print("⚠ Oxford Blue color not found in CSS")
                    return False
        else:
            print("✗ CSS file not found")
            return False
    except Exception as e:
        print(f"✗ Theme test error: {e}")
        return False

def test_env_config():
    """Test environment configuration"""
    print("\n" + "="*60)
    print("TEST 5: Environment Configuration")
    print("="*60)
    
    try:
        env_path = '.env'
        if os.path.exists(env_path):
            print("✓ .env file exists")
            
            with open(env_path, 'r') as f:
                content = f.read()
                
                if 'SECRET_KEY' in content:
                    print("✓ SECRET_KEY configured")
                
                if 'OPENAI_API_KEY' in content:
                    if content.count('OPENAI_API_KEY=sk-') > 0 and not content.startswith('#'):
                        print("✓ OpenAI API key configured")
                        print("✓ AI question generation enabled")
                    else:
                        print("⚠ OpenAI API key not configured")
                        print("\nTo enable AI generation:")
                        print("  1. Get key from https://platform.openai.com/api-keys")
                        print("  2. Add to .env: OPENAI_API_KEY=sk-your-key")
                        print("  3. Restart application")
                else:
                    print("⚠ OPENAI_API_KEY not in .env")
                
                return True
        else:
            print("✗ .env file not found")
            return False
    except Exception as e:
        print(f"✗ Environment config error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LEARNING APP SYSTEM TEST")
    print("="*60)
    
    results = []
    
    results.append(("Database", test_database()))
    results.append(("AI Engine", test_ai_engine()))
    results.append(("Question Generation", test_question_generation()))
    results.append(("Theme Files", test_theme()))
    results.append(("Environment Config", test_env_config()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All systems operational!")
        print("\nNext steps:")
        print("  1. Clear browser cache (Ctrl + F5)")
        print("  2. Start app: python run.py")
        print("  3. Test in browser: http://127.0.0.1:5000")
    else:
        print("\n⚠ Some tests failed - check output above")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
