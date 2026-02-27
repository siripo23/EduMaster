#!/usr/bin/env python3
"""
AI-Powered Question Generator
Extracts content from PDF question banks and generates new questions using AI
"""

import os
import json
import random
import pdfplumber
from openai import OpenAI
from typing import List, Dict
from models import Question

class AIQuestionGenerator:
    def __init__(self, api_key=None):
        """Initialize AI Question Generator"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        
        # Cache for extracted PDF content
        self.pdf_content_cache = {}
    
    def extract_pdf_content(self, pdf_path: str, max_pages: int = 50) -> str:
        """Extract text content from PDF"""
        if pdf_path in self.pdf_content_cache:
            return self.pdf_content_cache[pdf_path]
        
        try:
            content = []
            with pdfplumber.open(pdf_path) as pdf:
                # Extract from first max_pages pages
                for i, page in enumerate(pdf.pages[:max_pages]):
                    text = page.extract_text()
                    if text:
                        content.append(text)
            
            full_content = "\n\n".join(content)
            self.pdf_content_cache[pdf_path] = full_content
            return full_content
        
        except Exception as e:
            print(f"Error extracting PDF {pdf_path}: {e}")
            return ""
    
    def generate_questions_with_ai(
        self, 
        subject: str, 
        stream: str, 
        difficulty: str,
        num_questions: int = 5,
        topic: str = None
    ) -> List[Dict]:
        """Generate questions using AI based on PDF content"""
        
        if not self.client:
            print("OpenAI client not initialized. Using fallback method.")
            return self._generate_fallback_questions(subject, stream, difficulty, num_questions)
        
        # Get PDF path for the subject
        pdf_path = self._get_pdf_path(subject, stream)
        
        # Extract content from PDF
        pdf_content = self.extract_pdf_content(pdf_path)
        
        if not pdf_content:
            print(f"No content extracted from {pdf_path}")
            return self._generate_fallback_questions(subject, stream, difficulty, num_questions)
        
        # For large batches, generate in chunks of 10
        all_questions = []
        batch_size = 10
        
        for i in range(0, num_questions, batch_size):
            batch_count = min(batch_size, num_questions - i)
            
            # Create prompt for AI
            prompt = self._create_generation_prompt(
                subject, stream, difficulty, batch_count, topic, pdf_content
            )
            
            try:
                # Call OpenAI API (using gpt-3.5-turbo for cost efficiency)
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",  # 10x cheaper than gpt-4
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an expert {stream} exam question generator. Generate high-quality multiple-choice questions based on the provided content."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.8,  # Higher for more variety
                    max_tokens=3000
                )
                
                # Parse AI response
                questions_text = response.choices[0].message.content
                questions = self._parse_ai_response(questions_text, subject, stream, difficulty)
                
                all_questions.extend(questions)
                print(f"  ✓ Generated batch {i//batch_size + 1}: {len(questions)} questions")
            
            except Exception as e:
                print(f"Error calling OpenAI API (batch {i//batch_size + 1}): {e}")
                # Continue with next batch or use fallback
                continue
        
        # If we got enough questions, return them
        if len(all_questions) >= num_questions * 0.7:  # At least 70% success
            return all_questions[:num_questions]
        
        # Otherwise, use fallback
        print(f"AI generated only {len(all_questions)}/{num_questions} questions. Using fallback.")
        return self._generate_fallback_questions(subject, stream, difficulty, num_questions)
    
    def _create_generation_prompt(
        self, 
        subject: str, 
        stream: str, 
        difficulty: str,
        num_questions: int,
        topic: str,
        pdf_content: str
    ) -> str:
        """Create prompt for AI question generation"""
        
        # Limit PDF content to avoid token limits (use first 3000 chars as sample)
        content_sample = pdf_content[:3000]
        
        topic_instruction = f" focusing on the topic: {topic}" if topic else ""
        
        prompt = f"""Based on the following {stream} {subject} question bank content, generate {num_questions} NEW multiple-choice questions{topic_instruction}.

DIFFICULTY LEVEL: {difficulty}

REFERENCE CONTENT:
{content_sample}

REQUIREMENTS:
1. Generate {num_questions} completely NEW questions (not from the reference)
2. Each question should have 4 options (A, B, C, D)
3. Indicate the correct answer
4. Provide a brief explanation
5. Match the style and difficulty of {stream} {subject} exams
6. Difficulty level: {difficulty}

FORMAT YOUR RESPONSE EXACTLY AS:
---
QUESTION 1:
[Question text here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [A/B/C/D]
EXPLANATION: [Brief explanation]
TOPIC: [Specific topic name]
CHAPTER: [Chapter name]
---

Generate all {num_questions} questions following this exact format."""
        
        return prompt
    
    def _parse_ai_response(
        self, 
        response_text: str, 
        subject: str, 
        stream: str, 
        difficulty: str
    ) -> List[Dict]:
        """Parse AI-generated questions from response text"""
        
        questions = []
        
        # Split by question separator
        question_blocks = response_text.split('---')
        
        for block in question_blocks:
            if not block.strip() or 'QUESTION' not in block:
                continue
            
            try:
                # Extract question components
                lines = block.strip().split('\n')
                
                question_text = ""
                options = {'A': '', 'B': '', 'C': '', 'D': ''}
                correct_answer = ""
                explanation = ""
                topic = "General"
                chapter = "General"
                
                for line in lines:
                    line = line.strip()
                    
                    if line.startswith('QUESTION'):
                        continue
                    elif line.startswith('A)'):
                        options['A'] = line[2:].strip()
                    elif line.startswith('B)'):
                        options['B'] = line[2:].strip()
                    elif line.startswith('C)'):
                        options['C'] = line[2:].strip()
                    elif line.startswith('D)'):
                        options['D'] = line[2:].strip()
                    elif line.startswith('ANSWER:'):
                        correct_answer = line.replace('ANSWER:', '').strip()
                    elif line.startswith('EXPLANATION:'):
                        explanation = line.replace('EXPLANATION:', '').strip()
                    elif line.startswith('TOPIC:'):
                        topic = line.replace('TOPIC:', '').strip()
                    elif line.startswith('CHAPTER:'):
                        chapter = line.replace('CHAPTER:', '').strip()
                    elif not any(line.startswith(x) for x in ['A)', 'B)', 'C)', 'D)', 'ANSWER', 'EXPLANATION', 'TOPIC', 'CHAPTER']):
                        if question_text:
                            question_text += " " + line
                        else:
                            question_text = line
                
                # Validate question
                if question_text and all(options.values()) and correct_answer:
                    questions.append({
                        'subject': subject,
                        'chapter': chapter,
                        'topic': topic,
                        'difficulty': difficulty,
                        'question_text': question_text,
                        'option_a': options['A'],
                        'option_b': options['B'],
                        'option_c': options['C'],
                        'option_d': options['D'],
                        'correct_answer': correct_answer.upper()[0],  # Get first letter
                        'explanation': explanation,
                        'stream': stream
                    })
            
            except Exception as e:
                print(f"Error parsing question block: {e}")
                continue
        
        return questions
    
    def _get_pdf_path(self, subject: str, stream: str) -> str:
        """Get PDF path for subject and stream"""
        pdf_map = {
            'NEET': {
                'Physics': 'static/resources/NEET-PHYSICS.pdf',
                'Chemistry': 'static/resources/NEET-CHEMISTRY.pdf',
                'Biology': 'static/resources/NEET-BIOLOGY.pdf'
            },
            'JEE': {
                'Physics': 'static/resources/JEE-PHYSICS.pdf',
                'Chemistry': 'static/resources/JEE-CHEMISTRY.pdf',
                'Mathematics': 'static/resources/JEE-MATHS.pdf'
            }
        }
        
        return pdf_map.get(stream, {}).get(subject, '')
    
    def _generate_fallback_questions(
        self, 
        subject: str, 
        stream: str, 
        difficulty: str,
        num_questions: int
    ) -> List[Dict]:
        """Fallback method when AI is not available"""
        
        # Return empty list - will use existing database questions
        print(f"Fallback: No AI-generated questions. Using database questions.")
        return []
    
    def generate_test_questions(
        self,
        stream: str,
        test_type: str,
        num_questions: int = 30,
        user_weak_topics: Dict = None
    ) -> List[Dict]:
        """Generate questions for a complete test"""
        
        subjects = self._get_subjects_for_stream(stream)
        questions_per_subject = num_questions // len(subjects)
        
        all_questions = []
        
        for subject in subjects:
            # Determine difficulty distribution
            if test_type == 'initial':
                difficulties = ['Easy'] * (questions_per_subject // 3) + \
                              ['Medium'] * (questions_per_subject // 3) + \
                              ['Hard'] * (questions_per_subject - 2 * (questions_per_subject // 3))
            elif test_type == 'adaptive':
                # More medium and hard for adaptive
                difficulties = ['Easy'] * (questions_per_subject // 4) + \
                              ['Medium'] * (questions_per_subject // 2) + \
                              ['Hard'] * (questions_per_subject - questions_per_subject // 4 - questions_per_subject // 2)
            else:
                difficulties = ['Medium'] * questions_per_subject
            
            # Generate questions for each difficulty
            for difficulty in set(difficulties):
                count = difficulties.count(difficulty)
                questions = self.generate_questions_with_ai(
                    subject=subject,
                    stream=stream,
                    difficulty=difficulty,
                    num_questions=count
                )
                all_questions.extend(questions)
        
        # Shuffle questions
        random.shuffle(all_questions)
        
        return all_questions[:num_questions]
    
    def _get_subjects_for_stream(self, stream: str) -> List[str]:
        """Get subjects for stream"""
        if stream == 'NEET':
            return ['Physics', 'Chemistry', 'Biology']
        elif stream == 'JEE':
            return ['Physics', 'Chemistry', 'Mathematics']
        return []


# Example usage
if __name__ == '__main__':
    # Initialize generator
    generator = AIQuestionGenerator()
    
    # Generate sample questions
    questions = generator.generate_questions_with_ai(
        subject='Physics',
        stream='NEET',
        difficulty='Medium',
        num_questions=3
    )
    
    print(f"\nGenerated {len(questions)} questions:")
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['question_text']}")
        print(f"   A) {q['option_a']}")
        print(f"   B) {q['option_b']}")
        print(f"   C) {q['option_c']}")
        print(f"   D) {q['option_d']}")
        print(f"   Answer: {q['correct_answer']}")
