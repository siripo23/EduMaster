#!/usr/bin/env python3
"""
Basic tests for the NEET/JEE Learning App
"""

import unittest
import tempfile
import os
from app import app
from models import db, User, Question
from config import TestingConfig

class LearningAppTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        app.config.from_object(TestingConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.test_user = User(
            name='Test User',
            email='test@example.com',
            password='hashed_password',
            class_level='PUC2',
            stream='NEET'
        )
        db.session.add(self.test_user)
        
        # Create test question
        self.test_question = Question(
            subject='Physics',
            chapter='Mechanics',
            topic='Laws of Motion',
            difficulty='Easy',
            question_text='What is the SI unit of force?',
            option_a='Newton',
            option_b='Joule',
            option_c='Watt',
            option_d='Pascal',
            correct_answer='A',
            explanation='The SI unit of force is Newton.',
            stream='NEET'
        )
        db.session.add(self.test_question)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_page(self):
        """Test the index page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI-Powered NEET/JEE Preparation', response.data)
    
    def test_signup_page(self):
        """Test the signup page loads"""
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Your Account', response.data)
    
    def test_login_page(self):
        """Test the login page loads"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Your Account', response.data)
    
    def test_user_creation(self):
        """Test user model creation"""
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.stream, 'NEET')
    
    def test_question_creation(self):
        """Test question model creation"""
        question = Question.query.filter_by(subject='Physics').first()
        self.assertIsNotNone(question)
        self.assertEqual(question.correct_answer, 'A')
        self.assertEqual(question.stream, 'NEET')
    
    def test_weak_strong_topics(self):
        """Test user weak/strong topics functionality"""
        user = User.query.first()
        
        # Test setting weak topics
        weak_topics = {'Physics': ['Mechanics', 'Thermodynamics']}
        user.set_weak_topics(weak_topics)
        db.session.commit()
        
        retrieved_weak = user.get_weak_topics()
        self.assertEqual(retrieved_weak, weak_topics)
        
        # Test setting strong topics
        strong_topics = {'Chemistry': ['Organic Chemistry']}
        user.set_strong_topics(strong_topics)
        db.session.commit()
        
        retrieved_strong = user.get_strong_topics()
        self.assertEqual(retrieved_strong, strong_topics)

class AIEngineTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up AI engine tests"""
        app.config.from_object(TestingConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        from ai_engine import AdaptiveTestEngine
        self.ai_engine = AdaptiveTestEngine()
        
        # Create test questions
        for i in range(10):
            question = Question(
                subject='Physics',
                chapter='Mechanics',
                topic=f'Topic {i}',
                difficulty='Easy',
                question_text=f'Test question {i}',
                option_a='A',
                option_b='B',
                option_c='C',
                option_d='D',
                correct_answer='A',
                stream='NEET'
            )
            db.session.add(question)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_subjects_for_stream(self):
        """Test subject retrieval for different streams"""
        neet_subjects = self.ai_engine._get_subjects_for_stream('NEET')
        self.assertEqual(neet_subjects, ['Physics', 'Chemistry', 'Biology'])
        
        jee_subjects = self.ai_engine._get_subjects_for_stream('JEE')
        self.assertEqual(jee_subjects, ['Physics', 'Chemistry', 'Mathematics'])
    
    def test_difficulty_weights(self):
        """Test difficulty weight configuration"""
        beginner_weights = self.ai_engine.difficulty_weights['Beginner']
        self.assertEqual(beginner_weights['Easy'], 0.6)
        self.assertEqual(beginner_weights['Medium'], 0.3)
        self.assertEqual(beginner_weights['Hard'], 0.1)

def run_tests():
    """Run all tests"""
    print("Running NEET/JEE Learning App Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(LearningAppTestCase))
    suite.addTests(loader.loadTestsFromTestCase(AIEngineTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print results
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)