import random
import os
from models import Question, User, TestAttempt
from collections import defaultdict

# Try to import AI question generator
try:
    from ai_question_generator import AIQuestionGenerator
    AI_GENERATOR_AVAILABLE = True
except ImportError:
    AI_GENERATOR_AVAILABLE = False
    print("AI Question Generator not available. Using database questions only.")

class AdaptiveTestEngine:
    def __init__(self):
        self.difficulty_weights = {
            'Beginner': {'Easy': 0.6, 'Medium': 0.3, 'Hard': 0.1},
            'Intermediate': {'Easy': 0.3, 'Medium': 0.5, 'Hard': 0.2},
            'Advanced': {'Easy': 0.1, 'Medium': 0.4, 'Hard': 0.5}
        }
        
        # Initialize AI question generator if available
        self.ai_generator = None
        if AI_GENERATOR_AVAILABLE:
            try:
                self.ai_generator = AIQuestionGenerator()
                print("AI Question Generator initialized successfully")
            except Exception as e:
                print(f"Failed to initialize AI Generator: {e}")
                self.ai_generator = None
    
    def generate_initial_test(self, stream, num_questions=25):
        """Generate initial level detection test using AI or database"""
        subjects = self._get_subjects_for_stream(stream)
        questions_per_subject = num_questions // len(subjects)
        
        selected_questions = []
        used_ids = set()  # Track used question IDs to prevent duplicates
        
        for subject in subjects:
            # Get balanced questions across difficulties (more medium and hard)
            easy_count = int(questions_per_subject * 0.25)  # 25% easy
            medium_count = int(questions_per_subject * 0.40)  # 40% medium
            hard_count = questions_per_subject - easy_count - medium_count  # 35% hard
            
            # Generate questions for each difficulty
            for difficulty, count in [('Easy', easy_count), ('Medium', medium_count), ('Hard', hard_count)]:
                questions = self._generate_questions_ai_or_db(subject, stream, difficulty, count)
                # Filter out duplicates
                for q in questions:
                    if q.id not in used_ids:
                        selected_questions.append(q)
                        used_ids.add(q.id)
        
        random.shuffle(selected_questions)
        return selected_questions[:num_questions]
    
    def generate_adaptive_test(self, user, num_questions=30):
        """Generate adaptive test based on user's weak areas and level using AI"""
        weak_topics = user.get_weak_topics()
        user_level = user.level
        stream = user.stream
        
        # Get difficulty distribution based on user level (more challenging)
        if user_level == 'Beginner':
            difficulty_dist = {'Easy': 0.30, 'Medium': 0.45, 'Hard': 0.25}
        elif user_level == 'Intermediate':
            difficulty_dist = {'Easy': 0.20, 'Medium': 0.45, 'Hard': 0.35}
        else:  # Advanced
            difficulty_dist = {'Easy': 0.10, 'Medium': 0.40, 'Hard': 0.50}
        
        selected_questions = []
        used_ids = set()  # Track used question IDs to prevent duplicates
        subjects = self._get_subjects_for_stream(stream)
        
        # Calculate questions per subject
        questions_per_subject = num_questions // len(subjects)
        
        for subject in subjects:
            # Distribute questions by difficulty
            for difficulty, weight in difficulty_dist.items():
                difficulty_count = int(questions_per_subject * weight)
                
                if difficulty_count > 0:
                    questions = self._generate_questions_ai_or_db(
                        subject, stream, difficulty, difficulty_count
                    )
                    # Filter out duplicates
                    for q in questions:
                        if q.id not in used_ids:
                            selected_questions.append(q)
                            used_ids.add(q.id)
        
        random.shuffle(selected_questions)
        return selected_questions[:num_questions]
    
    def analyze_test_performance(self, user, test_attempt):
        """Analyze test performance and update user's weak/strong topics"""
        questions_attempted = test_attempt.get_questions_attempted()
        answers_given = test_attempt.get_answers_given()
        
        # Get questions from database
        questions = Question.query.filter(Question.id.in_(questions_attempted)).all()
        question_dict = {q.id: q for q in questions}
        
        # Analyze performance by topic and subject
        topic_performance = defaultdict(lambda: {'correct': 0, 'total': 0})
        subject_performance = defaultdict(lambda: {'correct': 0, 'total': 0})
        
        for q_id in questions_attempted:
            question = question_dict.get(q_id)
            if not question:
                continue
                
            is_correct = answers_given.get(str(q_id)) == question.correct_answer
            
            # Update topic performance
            topic_key = f"{question.subject}:{question.topic}"
            topic_performance[topic_key]['total'] += 1
            if is_correct:
                topic_performance[topic_key]['correct'] += 1
            
            # Update subject performance
            subject_performance[question.subject]['total'] += 1
            if is_correct:
                subject_performance[question.subject]['correct'] += 1
        
        # Determine weak and strong topics (threshold: 60%)
        weak_topics = defaultdict(list)
        strong_topics = defaultdict(list)
        
        for topic_key, performance in topic_performance.items():
            subject, topic = topic_key.split(':', 1)
            accuracy = performance['correct'] / performance['total']
            
            if accuracy < 0.6:
                weak_topics[subject].append(topic)
            elif accuracy >= 0.8:
                strong_topics[subject].append(topic)
        
        # Update user profile
        user.set_weak_topics(dict(weak_topics))
        user.set_strong_topics(dict(strong_topics))
        
        # Update user level based on overall performance
        overall_score = test_attempt.score / test_attempt.total_questions
        if test_attempt.test_type == 'initial':
            if overall_score >= 0.8:
                user.level = 'Advanced'
            elif overall_score >= 0.6:
                user.level = 'Intermediate'
            else:
                user.level = 'Beginner'
            
            user.initial_test_score = test_attempt.score
        
        # Store subject-wise scores
        subject_scores = {}
        for subject, performance in subject_performance.items():
            subject_scores[subject] = {
                'score': performance['correct'],
                'total': performance['total'],
                'percentage': (performance['correct'] / performance['total']) * 100
            }
        
        test_attempt.set_subject_scores(subject_scores)
        
        return {
            'weak_topics': dict(weak_topics),
            'strong_topics': dict(strong_topics),
            'subject_scores': subject_scores,
            'overall_percentage': overall_score * 100
        }
    
    def _get_subjects_for_stream(self, stream):
        """Get subjects based on stream"""
        if stream == 'NEET':
            return ['Physics', 'Chemistry', 'Biology']
        elif stream == 'JEE':
            return ['Physics', 'Chemistry', 'Mathematics']
        return []
    
    def _generate_questions_ai_or_db(self, subject, stream, difficulty, count):
        """Generate questions using AI if available, otherwise use database"""
        
        if count <= 0:
            return []
        
        # Try AI generation first
        if self.ai_generator:
            try:
                ai_questions = self.ai_generator.generate_questions_with_ai(
                    subject=subject,
                    stream=stream,
                    difficulty=difficulty,
                    num_questions=count
                )
                
                if ai_questions and len(ai_questions) >= count * 0.7:  # At least 70% success
                    # Convert dict to Question objects
                    question_objects = []
                    for q_data in ai_questions[:count]:  # Take exactly count questions
                        # Create temporary Question object (not saved to DB)
                        q = Question(
                            id=random.randint(100000, 999999),  # Temporary ID
                            subject=q_data['subject'],
                            chapter=q_data['chapter'],
                            topic=q_data['topic'],
                            difficulty=q_data['difficulty'],
                            question_text=q_data['question_text'],
                            option_a=q_data['option_a'],
                            option_b=q_data['option_b'],
                            option_c=q_data['option_c'],
                            option_d=q_data['option_d'],
                            correct_answer=q_data['correct_answer'],
                            explanation=q_data.get('explanation', ''),
                            stream=q_data['stream']
                        )
                        question_objects.append(q)
                    
                    print(f"✓ Generated {len(question_objects)} AI questions for {subject} ({difficulty})")
                    
                    # If we still need more questions, get from database
                    if len(question_objects) < count:
                        needed = count - len(question_objects)
                        db_questions = Question.query.filter_by(
                            subject=subject,
                            stream=stream,
                            difficulty=difficulty
                        ).limit(needed * 2).all()
                        
                        if db_questions:
                            additional = random.sample(db_questions, min(needed, len(db_questions)))
                            question_objects.extend(additional)
                            print(f"✓ Added {len(additional)} database questions for {subject} ({difficulty})")
                    
                    return question_objects
            
            except Exception as e:
                print(f"AI generation failed: {e}. Falling back to database.")
        
        # Fallback to database questions - GET ALL AVAILABLE, THEN SAMPLE
        all_questions = Question.query.filter_by(
            subject=subject,
            stream=stream,
            difficulty=difficulty
        ).all()
        
        if all_questions:
            # Shuffle to ensure randomness
            random.shuffle(all_questions)
            # Take up to count questions (no duplicates)
            selected = all_questions[:min(count, len(all_questions))]
            print(f"✓ Using {len(selected)} database questions for {subject} ({difficulty})")
            return selected
        
        # If no questions for this exact difficulty, try other difficulties
        print(f"⚠ No {difficulty} questions for {subject}, trying other difficulties...")
        all_subject_questions = Question.query.filter_by(
            subject=subject,
            stream=stream
        ).all()
        
        if all_subject_questions:
            random.shuffle(all_subject_questions)
            selected = all_subject_questions[:min(count, len(all_subject_questions))]
            print(f"✓ Using {len(selected)} mixed difficulty questions for {subject}")
            return selected
        
        print(f"⚠ No questions available for {subject}")
        return []
    
    def get_chapter_wise_questions(self, stream, subject, chapter, difficulty=None, limit=20):
        """Get questions for chapter-wise tests"""
        query = Question.query.filter_by(
            stream=stream,
            subject=subject,
            chapter=chapter
        )
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        questions = query.limit(limit * 2).all()
        return random.sample(questions, min(limit, len(questions)))
    
    def generate_full_paper(self, stream):
        """Generate a full NEET/JEE paper (180 questions, 720 marks) using AI"""
        selected_questions = []
        used_ids = set()  # Track used question IDs to prevent duplicates
        
        if stream == 'NEET':
            # NEET: 45 Physics, 45 Chemistry, 90 Biology = 180 questions
            distribution = {'Physics': 45, 'Chemistry': 45, 'Biology': 90}
        else:
            # JEE: 60 Physics, 60 Chemistry, 60 Mathematics = 180 questions
            distribution = {'Physics': 60, 'Chemistry': 60, 'Mathematics': 60}
        
        print(f"\n🎯 Generating Full {stream} Paper (180 questions, 720 marks)...")
        
        for subject, count in distribution.items():
            # Get balanced questions across difficulties (more challenging)
            easy_count = int(count * 0.25)  # 25% easy
            medium_count = int(count * 0.45)  # 45% medium
            hard_count = count - easy_count - medium_count  # 30% hard
            
            print(f"  📚 {subject}: {count} questions (Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count})")
            
            # Generate questions using AI or database
            for difficulty, diff_count in [('Easy', easy_count), ('Medium', medium_count), ('Hard', hard_count)]:
                questions = self._generate_questions_ai_or_db(subject, stream, difficulty, diff_count)
                # Filter out duplicates
                for q in questions:
                    if q.id not in used_ids:
                        selected_questions.append(q)
                        used_ids.add(q.id)
        
        random.shuffle(selected_questions)
        print(f"✅ Full paper generated: {len(selected_questions)} unique questions\n")
        return selected_questions
    
    def generate_subject_test(self, stream, subject, num_questions=30):
        """Generate subject-specific test using AI"""
        # Ensure subject name is properly formatted
        subject = subject.strip().title()
        
        # Get balanced questions across difficulties (more challenging)
        easy_count = int(num_questions * 0.25)  # 25% easy
        medium_count = int(num_questions * 0.45)  # 45% medium
        hard_count = num_questions - easy_count - medium_count  # 30% hard
        
        print(f"\n🎯 Generating {subject} Test for {stream} ({num_questions} questions)...")
        print(f"  Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}")
        
        selected_questions = []
        used_ids = set()  # Track used question IDs to prevent duplicates
        
        # Generate questions using AI or database - ENSURE CORRECT SUBJECT
        for difficulty, count in [('Easy', easy_count), ('Medium', medium_count), ('Hard', hard_count)]:
            questions = self._generate_questions_ai_or_db(subject, stream, difficulty, count)
            # Filter out duplicates AND verify subject matches
            for q in questions:
                if q.id not in used_ids and q.subject == subject:
                    selected_questions.append(q)
                    used_ids.add(q.id)
        
        random.shuffle(selected_questions)
        print(f"✅ {subject} test generated: {len(selected_questions)} unique questions\n")
        return selected_questions[:num_questions]