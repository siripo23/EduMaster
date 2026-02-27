# PDF Question Generation - Implementation Note

## Current Status

### Resources Updated ✅
The database has been successfully updated with the correct PDF files:

**NEET Resources (12 total):**
- Question Banks: 3 (Physics, Chemistry, Biology)
- Textbooks: 9 (PUC 1st & 2nd year books)

**JEE Resources (13 total):**
- Question Banks: 3 (Physics, Chemistry, Mathematics)
- Textbooks: 10 (PUC 1st & 2nd year books)

### Question Generation from PDFs

To generate questions automatically from the PDF files, we would need to implement:

1. **PDF Text Extraction**
   - Use libraries like PyPDF2, pdfplumber, or PyMuPDF
   - Extract text content from question bank PDFs

2. **Question Parsing**
   - Identify question patterns
   - Extract question text, options (A, B, C, D)
   - Identify correct answers
   - Parse explanations if available

3. **Database Population**
   - Parse extracted questions
   - Categorize by subject, chapter, topic
   - Assign difficulty levels
   - Store in Question table

## Implementation Options

### Option 1: Manual Question Entry (Current)
- Continue using the existing 17 sample questions
- Manually add more questions to the database using `init_db.py`
- Pros: Accurate, controlled quality
- Cons: Time-consuming, limited quantity

### Option 2: PDF Parsing Script (Recommended)
Create a script to parse the question bank PDFs:

```python
import PyPDF2
import re
from models import db, Question

def parse_question_pdf(pdf_path, subject, stream):
    # Extract text from PDF
    # Parse questions using regex patterns
    # Identify question structure
    # Extract options and answers
    # Save to database
    pass
```

**Requirements:**
- Install: `pip install PyPDF2 pdfplumber`
- Define question patterns for NEET/JEE format
- Handle different question formats
- Validate extracted data

### Option 3: AI-Powered Question Generation
Use AI (like GPT) to:
- Read PDF content
- Generate similar questions
- Create variations of existing questions
- Ensure proper difficulty distribution

**Requirements:**
- OpenAI API key or similar
- PDF text extraction
- Prompt engineering for question generation
- Quality validation

### Option 4: OCR for Scanned PDFs
If PDFs are scanned images:
- Use Tesseract OCR or similar
- Extract text from images
- Parse extracted text
- More complex but handles image-based PDFs

## Current Workaround

For now, the application works with:
1. **17 sample questions** in the database (for testing)
2. **PDF downloads** available in Resources section
3. Users can download and study from the actual question banks

## Recommended Next Steps

1. **Inspect PDF Structure**
   - Open NEET-PHYSICS.pdf, JEE-MATHS.pdf, etc.
   - Check if they're text-based or scanned images
   - Identify question format/pattern

2. **Choose Parsing Method**
   - If text-based: Use PyPDF2/pdfplumber
   - If image-based: Use OCR (Tesseract)
   - If mixed: Combine both approaches

3. **Create Parsing Script**
   - Write script to extract questions
   - Test with one subject first
   - Validate accuracy
   - Scale to all subjects

4. **Populate Database**
   - Run parsing script
   - Import questions to database
   - Verify question quality
   - Test with actual tests

## Example Parsing Script Structure

```python
#!/usr/bin/env python3
"""
Parse NEET/JEE question bank PDFs and populate database
"""

import pdfplumber
import re
from app import app
from models import db, Question

def extract_questions_from_pdf(pdf_path, subject, stream):
    """Extract questions from PDF"""
    questions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # Parse questions using regex
            # Pattern depends on PDF format
            # Example: Question 1. What is...?
            # A) Option A
            # B) Option B
            # C) Option C
            # D) Option D
            # Answer: A
            
    return questions

def save_questions_to_db(questions):
    """Save parsed questions to database"""
    with app.app_context():
        for q_data in questions:
            question = Question(
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
            db.session.add(question)
        
        db.session.commit()
        print(f"Added {len(questions)} questions to database")

if __name__ == '__main__':
    # Parse NEET Physics
    questions = extract_questions_from_pdf(
        'static/resources/NEET-PHYSICS.pdf',
        'Physics',
        'NEET'
    )
    save_questions_to_db(questions)
```

## Current Application Status

The application is fully functional with:
- ✅ Resources page showing all PDFs
- ✅ Download functionality for all materials
- ✅ Test system working with sample questions
- ✅ All features operational

**To add more questions:** Either manually add them to `init_db.py` or implement PDF parsing as described above.

## Date
February 27, 2026
