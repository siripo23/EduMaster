import random
from models import Question, User, TestAttempt
from collections import defaultdict

class AdaptiveTestEngine:
    def __init__(self):
        self.difficulty_weights = {
            'Beginner': {'Easy': 0.6, 'Medium': 0.3, 'Hard': 0.1},
            'Intermediate': {'Easy': 0.3, 'Medium': 0.5, 'Hard': 0.2},
            'Advanced': {'Easy': 0.1, 'Medium': 0.4, 'Hard': 0.5}
        }
    
    def generate_initial_test(self, stream, num_questions=25):
        """Generate initial level detection test"""
        subjects = self._get_subjects_for_stream(stream)
        questions_per_subject = num_questions // len(subjects)
        
        selected_questions = []
        
        for subject in subjects:
            # Get balanced questions across difficulties
            easy_count = questions_per_subject // 3
            medium_count = questions_per_subject // 3
            hard_count = questions_per_subject - easy_count - medium_count
            
            easy_questions = Question.query.filter_by(
                subject=subject, stream=stream, difficulty='Easy'
            ).order_by(Question.id.desc()).limit(easy_count * 2).all()
            
            medium_questions = Question.query.filter_by(
                subject=subject, stream=stream, difficulty='Medium'
            ).order_by(Question.id.desc()).limit(medium_count * 2).all()
            
            hard_questions = Question.query.filter_by(
                subject=subject, stream=stream, difficulty='Hard'
            ).order_by(Question.id.desc()).limit(hard_count * 2).all()
            
            # Randomly select from available questions
            selected_questions.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
            selected_questions.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
            selected_questions.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
        
        random.shuffle(selected_questions)
        return selected_questions[:num_questions]
    
    def generate_adaptive_test(self, user, num_questions=30):
        """Generate adaptive test based on user's weak areas and level"""
        weak_topics = user.get_weak_topics()
        user_level = user.level
        stream = user.stream
        
        # Get difficulty distribution based on user level
        difficulty_dist = self.difficulty_weights[user_level]
        
        selected_questions = []
        subjects = self._get_subjects_for_stream(stream)
        
        # Calculate questions per subject
        questions_per_subject = num_questions // len(subjects)
        
        for subject in subjects:
            subject_questions = []
            
            # Get weak topics for this subject
            subject_weak_topics = weak_topics.get(subject, [])
            
            # Distribute questions by difficulty
            for difficulty, weight in difficulty_dist.items():
                difficulty_count = int(questions_per_subject * weight)
                
                if subject_weak_topics:
                    # Prioritize weak topics (70% of questions)
                    weak_topic_count = int(difficulty_count * 0.7)
                    general_count = difficulty_count - weak_topic_count
                    
                    # Get questions from weak topics
                    weak_questions = Question.query.filter(
                        Question.subject == subject,
                        Question.stream == stream,
                        Question.difficulty == difficulty,
                        Question.topic.in_(subject_weak_topics)
                    ).limit(weak_topic_count * 2).all()
                    
                    subject_questions.extend(random.sample(
                        weak_questions, min(weak_topic_count, len(weak_questions))
                    ))
                    
                    # Get general questions
                    general_questions = Question.query.filter(
                        Question.subject == subject,
                        Question.stream == stream,
                        Question.difficulty == difficulty
                    ).limit(general_count * 2).all()
                    
                    subject_questions.extend(random.sample(
                        general_questions, min(general_count, len(general_questions))
                    ))
                else:
                    # No weak topics identified, get general questions
                    general_questions = Question.query.filter(
                        Question.subject == subject,
                        Question.stream == stream,
                        Question.difficulty == difficulty
                    ).limit(difficulty_count * 2).all()
                    
                    subject_questions.extend(random.sample(
                        general_questions, min(difficulty_count, len(general_questions))
                    ))
            
            selected_questions.extend(subject_questions)
        
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
        """Generate a full NEET/JEE paper"""
        selected_questions = []
        
        if stream == 'NEET':
            # NEET: 45 Physics, 45 Chemistry, 90 Biology
            distribution = {'Physics': 45, 'Chemistry': 45, 'Biology': 90}
        else:
            # JEE: 60 Physics, 60 Chemistry, 60 Mathematics
            distribution = {'Physics': 60, 'Chemistry': 60, 'Mathematics': 60}
        
        for subject, count in distribution.items():
            # Get balanced questions across difficulties
            easy_count = int(count * 0.3)
            medium_count = int(count * 0.5)
            hard_count = count - easy_count - medium_count
            
            easy_questions = Question.query.filter_by(
                subject=subject,
                stream=stream,
                difficulty='Easy'
            ).order_by(Question.id.desc()).limit(easy_count * 2).all()
            
            medium_questions = Question.query.filter_by(
                subject=subject,
                stream=stream,
                difficulty='Medium'
            ).order_by(Question.id.desc()).limit(medium_count * 2).all()
            
            hard_questions = Question.query.filter_by(
                subject=subject,
                stream=stream,
                difficulty='Hard'
            ).order_by(Question.id.desc()).limit(hard_count * 2).all()
            
            # Randomly select from available questions
            selected_questions.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
            selected_questions.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
            selected_questions.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
        
        random.shuffle(selected_questions)
        return selected_questions
    
    def generate_subject_test(self, stream, subject, num_questions=30):
        """Generate subject-specific test"""
        # Get balanced questions across difficulties
        easy_count = int(num_questions * 0.3)
        medium_count = int(num_questions * 0.5)
        hard_count = num_questions - easy_count - medium_count
        
        selected_questions = []
        
        easy_questions = Question.query.filter_by(
            subject=subject,
            stream=stream,
            difficulty='Easy'
        ).order_by(Question.id.desc()).limit(easy_count * 2).all()
        
        medium_questions = Question.query.filter_by(
            subject=subject,
            stream=stream,
            difficulty='Medium'
        ).order_by(Question.id.desc()).limit(medium_count * 2).all()
        
        hard_questions = Question.query.filter_by(
            subject=subject,
            stream=stream,
            difficulty='Hard'
        ).order_by(Question.id.desc()).limit(hard_count * 2).all()
        
        # Randomly select from available questions
        selected_questions.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
        selected_questions.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
        selected_questions.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
        
        random.shuffle(selected_questions)
        return selected_questions[:num_questions]