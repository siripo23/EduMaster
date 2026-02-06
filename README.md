# AI-Based Adaptive Learning & Test Generation App

A web-based application for PUC students preparing for NEET or JEE exams with personalized learning and adaptive test generation.

## Features

- User authentication and profile management
- Stream selection (NEET/JEE)
- Initial level detection test
- AI-based adaptive paper generation
- Learning resources (PDFs, past papers)
- Performance tracking

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite
- AI Logic: Rule-based adaptive system

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python init_db.py`
3. Run application: `python simple_app.py`

## Project Structure

```
├── app.py              # Main Flask application
├── models.py           # Database models
├── ai_engine.py        # Adaptive test generation logic
├── init_db.py          # Database initialization
├── requirements.txt    # Python dependencies
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── data/              # Question banks, PDFs
└── uploads/           # User uploaded content
```