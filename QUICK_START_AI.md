# Quick Start: AI Question Generation

## 🚀 Get Started in 5 Minutes

### Step 1: Install New Packages

```bash
pip install openai pdfplumber
```

### Step 2: Get OpenAI API Key

1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### Step 3: Add API Key to .env

Create or edit `.env` file in project root:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Restart Application

```bash
python run.py
```

### Step 5: Take Any Test!

1. Go to http://127.0.0.1:5000
2. Login
3. Choose any test type:
   - **Adaptive Test** (30 questions)
   - **Full Mock Paper** (180 questions, 720 marks!)
   - **Subject-wise Test** (Physics/Chemistry/Biology)
4. Watch the AI magic happen! ✨

## What You'll See

### For Adaptive Test (30 questions):
```
Console Output:
✓ AI Question Generator initialized successfully
✓ Generated 8 AI questions for Physics (Medium)
✓ Generated 7 AI questions for Chemistry (Easy)
✓ Generated 10 AI questions for Biology (Medium)
✓ Generated 5 AI questions for Physics (Hard)
```

### For Full Mock Paper (180 questions, 720 marks):
```
Console Output:
🎯 Generating Full NEET Paper (180 questions, 720 marks)...
  📚 Physics: 45 questions (Easy: 14, Medium: 23, Hard: 8)
  ✓ Generated batch 1: 10 questions
  ✓ Generated batch 2: 10 questions
  ✓ Generated batch 3: 10 questions
  ✓ Generated batch 4: 10 questions
  ✓ Generated batch 5: 5 questions
  📚 Chemistry: 45 questions (Easy: 14, Medium: 23, Hard: 8)
  ✓ Generated batch 1: 10 questions
  ...
  📚 Biology: 90 questions (Easy: 27, Medium: 45, Hard: 18)
  ...
✅ Full paper generated: 180 questions
```

### For Subject Test (30 questions):
```
Console Output:
🎯 Generating Physics Test (30 questions)...
  Easy: 9, Medium: 15, Hard: 6
✓ Generated batch 1: 10 questions
✓ Generated batch 2: 10 questions
✓ Generated batch 3: 10 questions
✅ Physics test generated: 30 questions
```

## How It Works

1. **You click "Start Test"**
2. **AI reads your PDF question banks** (NEET-PHYSICS.pdf, JEE-MATHS.pdf, etc.)
3. **GPT-4 generates brand new questions** in batches
4. **Questions appear in test interface**
5. **Every test has completely different questions!**

## All Test Types Supported

✅ **Adaptive Tests** - 30 questions, personalized
✅ **Full Mock Papers** - 180 questions, 720 marks (complete NEET/JEE exam)
✅ **Subject-wise Tests** - 30 questions per subject
✅ **Initial Assessment** - 25 questions, level detection

## Cost

### GPT-4 (Higher Quality):
- **Adaptive Test:** ~$0.10 - $0.15
- **Subject Test:** ~$0.10 - $0.15
- **Full Paper:** ~$0.60 - $0.90
- **100 Tests:** ~$10 - $15

### GPT-3.5 (Recommended - 10x Cheaper):
- **Adaptive Test:** ~$0.01 - $0.02
- **Subject Test:** ~$0.01 - $0.02
- **Full Paper:** ~$0.06 - $0.09
- **100 Tests:** ~$1 - $2

### To Use GPT-3.5:
Edit `ai_question_generator.py`, line 85:
```python
model="gpt-3.5-turbo"  # Instead of "gpt-4"
```

## Without API Key?

No problem! The app automatically falls back to database questions.

## Features

✅ Unlimited unique questions for ALL test types
✅ Never repeats questions
✅ Learns from your PDF question banks
✅ Maintains NEET/JEE exam standards
✅ Generates 720 marks full papers
✅ Works offline (fallback mode)

## Need Help?

Check these guides:
- `AI_COMPLETE_IMPLEMENTATION.md` - Full documentation
- `AI_QUESTION_GENERATION_SETUP.md` - Detailed setup

---

**That's it! You're ready to generate infinite NEET/JEE questions for all test types! 🎉**

**Including full 180-question, 720-marks mock papers!**

