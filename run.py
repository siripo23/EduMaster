#!/usr/bin/env python3
"""
Production-ready runner for the NEET/JEE Learning App
"""

import os
from app import app
from models import db

def create_app():
    """Create and configure the Flask application"""
    
    # Create upload directories if they don't exist
    upload_dirs = ['uploads', 'data', 'static/resources']
    for directory in upload_dirs:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize database
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Create app
    application = create_app()
    
    print(f"Starting NEET/JEE Learning App...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Running on: http://{host}:{port}")
    
    # Run the application
    application.run(host=host, port=port, debug=debug)