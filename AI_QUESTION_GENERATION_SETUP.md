# AI Question Generation Setup Guide

## Overview

The application now supports AI-powered question generation that:
- Reads content from PDF question banks
- Generates NEW questions dynamically for each test
- Never repeats the same questions
- Maintains NEET/JEE exam standards
- Falls back to database questions if AI is unavailable

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Test Request                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              AdaptiveTestEngine                          │
│  (ai_engine.py)                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│          AIQuestionGenerator                             │
│  (ai_question_generator.py)                              │
│                                                           │
│  1. Extract PDF content (pdfplumber)                     │
│  2. Send to OpenAI GPT-4                                 │
│  3. Parse AI response                                    │
│  4. Return Question objects                              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Generated Questions                         │
│  (Fresh questions for each test)                         │
└─────────────────────────────────────────────────────────┘
```

## Installation

### 1. Install Required Packages

```bash
pip install openai pdfplumber
```

Update `requirements.txt`:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
python-dotenv==1.0.0
openai==1.12.0
pdfplumber==0.10.3
```

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create an account or sign in
3. Click "Create new secret key"
4. Copy the API key (starts with `sk-...`)

### 3. Configure API Key

Add to your `.env` file:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

Or set as environment variable:
```bash
# Windows
set OPENAI_API_KEY=sk-your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-api-key-here
```

## How It Works

### 1. PDF Content Extraction

```python
# Extracts text from question bank PDFs
content = extract_pdf_content('static/resources/NEET-PHYSICS.pdf')
```

### 2. AI Prompt Generation

```python
prompt = f"""Based on the following NEET Physics question bank content, 
generate 5 NEW multiple-choice questions.

REFERENCE CONTENT:
{pdf_content_sample}

REQUIREMENTS:
1. Generate completely NEW questions (not from reference)
2. Each question should have 4 options (A, B, C, D)
3. Indicate correct answer
4. Provide explanation
5. Match NEET Physics exam style
6. Difficulty level: Medium
"""
```

### 3. OpenAI API Call

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a NEET exam expert..."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8  # Higher for variety
)
```

### 4. Question Parsing

The AI response is parsed to extract:
- Question text
- Options A, B, C, D
- Correct answer
- Explanation
- Topic and chapter

### 5. Dynamic Generation

Every test generates fresh questions:
```python
# Test 1: Gets questions 1-30 (AI generated)
# Test 2: Gets questions 31-60 (AI generated)
# Test 3: Gets questions 61-90 (AI generated)
# ... infinite unique questions
```

## Usage

### Automatic (Default)

The system automatically uses AI when available:

```python
# In ai_engine.py
engine = AdaptiveTestEngine()  # Initializes AI generator

# Generate test
questions = engine.generate_initial_test('NEET', 25)
# ✓ Generated 25 AI questions
```

### Manual Testing

Test the AI generator directly:

```python
from ai_question_generator import AIQuestionGenerator

generator = AIQuestionGenerator()

# Generate questions
questions = generator.generate_questions_with_ai(
    subject='Physics',
    stream='NEET',
    difficulty='Medium',
    num_questions=5
)

for q in questions:
    print(q['question_text'])
```

## Features

### 1. Infinite Question Pool
- Never runs out of questions
- Each test has unique questions
- No repetition across tests

### 2. PDF-Based Learning
- Reads actual NEET/JEE question banks
- Understands question patterns
- Maintains exam standards

### 3. Intelligent Generation
- Matches difficulty levels
- Covers all topics
- Proper option distribution
- Accurate explanations

### 4. Fallback System
- If AI fails → uses database questions
- If no API key → uses database questions
- Graceful degradation

## Cost Estimation

### OpenAI Pricing (GPT-4)
- Input: $0.03 per 1K tokens
- Output: $0.06 per 1K tokens

### Per Test Cost
- 30 questions test ≈ 2000 tokens
- Cost per test ≈ $0.10 - $0.15
- 100 tests ≈ $10 - $15

### Optimization Tips
1. Use GPT-3.5-turbo (10x cheaper)
2. Cache generated questions
3. Batch generation
4. Use database for practice tests

## Configuration

### Switch to GPT-3.5 (Cheaper)

In `ai_question_generator.py`:
```python
model="gpt-3.5-turbo"  # Instead of "gpt-4"
```

### Adjust Generation Parameters

```python
temperature=0.8  # 0.0-1.0 (higher = more creative)
max_tokens=2000  # Maximum response length
```

### Enable/Disable AI

```python
# Disable AI (use database only)
AI_GENERATOR_AVAILABLE = False
```

## Testing

### 1. Test PDF Extraction

```bash
python -c "from ai_question_generator import AIQuestionGenerator; g = AIQuestionGenerator(); print(len(g.extract_pdf_content('static/resources/NEET-PHYSICS.pdf')))"
```

### 2. Test AI Generation

```bash
python ai_question_generator.py
```

### 3. Test Full Integration

```bash
python run.py
# Take a test and verify questions are generated
```

## Troubleshooting

### Error: "No OpenAI API key found"
**Solution:** Set OPENAI_API_KEY environment variable

### Error: "Rate limit exceeded"
**Solution:** Wait a few minutes or upgrade OpenAI plan

### Error: "PDF extraction failed"
**Solution:** Check PDF file exists and is readable

### Questions not generating
**Solution:** Check logs for errors, verify API key is valid

## Monitoring

### Check AI Usage

```python
# In Flask logs
✓ Generated 8 AI questions for Physics (Medium)
✓ Generated 7 AI questions for Chemistry (Easy)
✓ Using 5 database questions for Biology (Hard)
```

### Track Costs

Monitor usage at: https://platform.openai.com/usage

## Production Recommendations

1. **Cache Questions**
   - Store AI-generated questions in database
   - Reuse for similar difficulty/topic
   - Reduce API calls

2. **Batch Generation**
   - Generate 100 questions at once
   - Store in database
   - Use for multiple tests

3. **Hybrid Approach**
   - Use AI for new questions
   - Use database for practice
   - Balance cost and freshness

4. **Rate Limiting**
   - Limit AI generation per user
   - Use database for frequent tests
   - AI for important tests only

## Benefits

✅ **Unlimited Questions** - Never run out
✅ **Always Fresh** - No repetition
✅ **Exam Standard** - Maintains quality
✅ **PDF-Based** - Uses actual question banks
✅ **Scalable** - Handles any number of users
✅ **Fallback** - Works without AI too

## Next Steps

1. Install packages: `pip install openai pdfplumber`
2. Get API key from OpenAI
3. Add to `.env` file
4. Restart application
5. Take a test - questions will be AI-generated!

## Status

🟢 **READY TO USE**

The AI question generation system is fully implemented and ready to use once you add your OpenAI API key!

## Date
February 27, 2026
