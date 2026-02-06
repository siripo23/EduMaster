#!/usr/bin/env python3
"""
Setup script for NEET/JEE Learning App
Handles initial setup, database initialization, and sample data creation
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        'uploads',
        'data',
        'static/resources',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  Created: {directory}")
    
    print("✅ Directories created successfully!")

def initialize_database():
    """Initialize database with sample data"""
    print("Initializing database...")
    try:
        subprocess.check_call([sys.executable, 'init_db.py'])
        print("✅ Database initialized successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing database: {e}")
        return False

def create_env_file():
    """Create environment configuration file"""
    env_content = """# NEET/JEE Learning App Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///learning_app.db
HOST=127.0.0.1
PORT=5000
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment file (.env) created!")
    else:
        print("ℹ️  Environment file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up NEET/JEE Learning App...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    success = True
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Create environment file
    create_env_file()
    
    # Step 3: Install requirements
    if not install_requirements():
        success = False
    
    # Step 4: Initialize database
    if success and not initialize_database():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Review and update the .env file with your configuration")
        print("2. Run the application:")
        print("   python run.py")
        print("   or")
        print("   python app.py")
        print("\n3. Access the app at: http://127.0.0.1:5000")
        print("\n4. Use admin.py to add more questions and resources")
    else:
        print("❌ Setup failed! Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()