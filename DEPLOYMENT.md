# NEET/JEE Learning App - Deployment Guide

## Quick Start

### 1. Setup
```bash
# Clone or download the project
cd neet-jee-learning-app

# Run the setup script
python setup.py
```

### 2. Run the Application
```bash
# Development mode
python run.py

# Or directly
python app.py
```

### 3. Access the App
Open your browser and go to: `http://127.0.0.1:5000`

## Manual Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Directories**
   ```bash
   mkdir uploads data static/resources logs
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///learning_app.db
HOST=127.0.0.1
PORT=5000
```

### Configuration Options
- `FLASK_ENV`: Set to `production` for production deployment
- `SECRET_KEY`: Change this to a secure random key for production
- `DATABASE_URL`: Database connection string
- `HOST`: Server host (use `0.0.0.0` for external access)
- `PORT`: Server port

## Database Management

### Initialize Database
```bash
python init_db.py
```

### Add Questions and Resources
```bash
python admin.py
```

The admin interface allows you to:
- Add individual questions
- Add resources (textbooks, past papers)
- Bulk import questions from JSON
- View database statistics

### Sample JSON Format for Bulk Import
```json
[
  {
    "subject": "Physics",
    "chapter": "Mechanics",
    "topic": "Laws of Motion",
    "difficulty": "Easy",
    "question_text": "What is Newton's first law?",
    "option_a": "Law of Inertia",
    "option_b": "Law of Acceleration",
    "option_c": "Law of Action-Reaction",
    "option_d": "Law of Gravitation",
    "correct_answer": "A",
    "explanation": "Newton's first law is also known as the Law of Inertia.",
    "stream": "NEET"
  }
]
```

## Production Deployment

### 1. Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:application
```

### 2. Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python init_db.py

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:application"]
```

Build and run:
```bash
docker build -t neet-jee-app .
docker run -p 5000:5000 neet-jee-app
```

### 3. Environment Configuration for Production
```env
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
HOST=0.0.0.0
PORT=5000
```

## File Structure
```
neet-jee-learning-app/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── ai_engine.py           # Adaptive test generation logic
├── config.py              # Configuration settings
├── init_db.py             # Database initialization
├── admin.py               # Admin interface
├── run.py                 # Production runner
├── setup.py               # Setup script
├── test_app.py            # Basic tests
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── test.html
│   ├── test_results.html
│   ├── resources.html
│   └── profile.html
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── resources/         # PDF files, images
├── data/                  # Question banks, additional data
├── uploads/               # User uploaded files
└── logs/                  # Application logs
```

## Testing

Run the test suite:
```bash
python test_app.py
```

## Features

### User Management
- User registration and authentication
- Profile management with performance tracking
- Stream selection (NEET/JEE)
- Class level selection (PUC1/PUC2)

### Adaptive Testing System
- Initial level detection test
- AI-based adaptive question paper generation
- Performance analysis and weak area identification
- Subject-wise scoring and progress tracking

### Learning Resources
- Textbook PDFs organized by subject and chapter
- Past year question papers
- Chapter-wise practice tests

### AI Engine Features
- Rule-based adaptive algorithm
- Difficulty adjustment based on user level
- Weak topic prioritization
- Performance trend analysis

## Troubleshooting

### Common Issues

1. **Database not found**
   ```bash
   python init_db.py
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission errors**
   - Ensure write permissions for uploads/ and data/ directories

4. **Port already in use**
   - Change PORT in .env file or kill the process using the port

### Logs
Check application logs in the `logs/` directory for detailed error information.

## Security Considerations

### For Production:
1. Change the SECRET_KEY to a secure random value
2. Use HTTPS in production
3. Set up proper database backups
4. Implement rate limiting
5. Use environment variables for sensitive configuration
6. Regular security updates

### Database Security:
- Use PostgreSQL or MySQL for production instead of SQLite
- Implement proper user permissions
- Regular backups and recovery testing

## Performance Optimization

### Database:
- Add indexes for frequently queried fields
- Use database connection pooling
- Implement query optimization

### Caching:
- Implement Redis for session storage
- Cache frequently accessed questions
- Use CDN for static files

### Monitoring:
- Set up application monitoring
- Log performance metrics
- Monitor database performance

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Ensure all dependencies are installed correctly
4. Verify database initialization completed successfully

## License

This project is for educational purposes. Please ensure compliance with any applicable licenses for educational content and examination materials.