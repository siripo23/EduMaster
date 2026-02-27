#!/usr/bin/env python3
"""
Update resources in database with correct PDF files
"""

from app import app
from models import db, Resource

def update_resources():
    """Update resources with correct PDF files"""
    
    with app.app_context():
        # Clear existing resources
        Resource.query.delete()
        db.session.commit()
        print("Cleared existing resources")
        
        resources = []
        
        # NEET Resources
        neet_resources = [
            # NEET Past Papers (Main Question Papers)
            {
                'title': 'NEET Physics Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Physics',
                'file_path': '/static/resources/NEET-PHYSICS.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': 'NEET Chemistry Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Chemistry',
                'file_path': '/static/resources/NEET-CHEMISTRY.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': 'NEET Biology Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Biology',
                'file_path': '/static/resources/NEET-BIOLOGY.pdf',
                'stream': 'NEET',
                'year': None
            },
            # NEET Textbooks
            {
                'title': '1st PUC Biology Textbook',
                'resource_type': 'textbook',
                'subject': 'Biology',
                'file_path': '/static/resources/1st pu- Biology.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '2nd PUC Biology Textbook',
                'resource_type': 'textbook',
                'subject': 'Biology',
                'file_path': '/static/resources/2nd Biology.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '1st PUC Chemistry Part-1',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/1st PUC-Chemistry-Part-1.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '1st PUC Chemistry Part-2',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/1 PUC Chemistry Part-2.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '2nd PUC Chemistry Part-1',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/2nd PUC-Chemistry-Part-1.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '2nd PUC Chemistry Part-2',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/2 PUC Chemistry Part-2.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '1st PUC Physics Part-1',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/1 PUC Physics Part-1.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '1st PUC Physics Part-2',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/1PUC Physics Part-2.pdf',
                'stream': 'NEET',
                'year': None
            },
            {
                'title': '2nd PUC Physics Part-1',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/2nd PUC - Physics- Part-1.pdf',
                'stream': 'NEET',
                'year': None
            },
        ]
        
        # JEE Resources
        jee_resources = [
            # JEE Past Papers (Main Question Papers)
            {
                'title': 'JEE Physics Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Physics',
                'file_path': '/static/resources/JEE-PHYSICS.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': 'JEE Chemistry Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Chemistry',
                'file_path': '/static/resources/JEE-CHEMISTRY.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': 'JEE Mathematics Question Bank',
                'resource_type': 'past_paper',
                'subject': 'Mathematics',
                'file_path': '/static/resources/JEE-MATHS.pdf',
                'stream': 'JEE',
                'year': None
            },
            # JEE Textbooks
            {
                'title': '1st PUC Mathematics Textbook',
                'resource_type': 'textbook',
                'subject': 'Mathematics',
                'file_path': '/static/resources/1Puc Maths.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '2nd PUC Mathematics Part-1',
                'resource_type': 'textbook',
                'subject': 'Mathematics',
                'file_path': '/static/resources/2 puc maths-part 1.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '2nd PUC Mathematics Part-2',
                'resource_type': 'textbook',
                'subject': 'Mathematics',
                'file_path': '/static/resources/2nd puc maths part 2.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '1st PUC Chemistry Part-1',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/1st PUC-Chemistry-Part-1.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '1st PUC Chemistry Part-2',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/1 PUC Chemistry Part-2.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '2nd PUC Chemistry Part-1',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/2nd PUC-Chemistry-Part-1.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '2nd PUC Chemistry Part-2',
                'resource_type': 'textbook',
                'subject': 'Chemistry',
                'file_path': '/static/resources/2 PUC Chemistry Part-2.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '1st PUC Physics Part-1',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/1 PUC Physics Part-1.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '1st PUC Physics Part-2',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/1PUC Physics Part-2.pdf',
                'stream': 'JEE',
                'year': None
            },
            {
                'title': '2nd PUC Physics Part-1',
                'resource_type': 'textbook',
                'subject': 'Physics',
                'file_path': '/static/resources/2nd PUC - Physics- Part-1.pdf',
                'stream': 'JEE',
                'year': None
            },
        ]
        
        resources.extend(neet_resources)
        resources.extend(jee_resources)
        
        # Add resources to database
        added_count = 0
        
        for resource_data in resources:
            resource = Resource(**resource_data)
            db.session.add(resource)
            added_count += 1
            print(f"✓ Added: {resource_data['title']} ({resource_data['stream']})")
        
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"Resources updated successfully!")
        print(f"✓ Total resources added: {added_count}")
        print(f"{'='*60}")
        
        # Show breakdown by stream
        neet_count = Resource.query.filter_by(stream='NEET').count()
        jee_count = Resource.query.filter_by(stream='JEE').count()
        
        neet_textbooks = Resource.query.filter_by(stream='NEET', resource_type='textbook').count()
        neet_papers = Resource.query.filter_by(stream='NEET', resource_type='past_paper').count()
        
        jee_textbooks = Resource.query.filter_by(stream='JEE', resource_type='textbook').count()
        jee_papers = Resource.query.filter_by(stream='JEE', resource_type='past_paper').count()
        
        print(f"\n📚 Resources by Stream:")
        print(f"   NEET: {neet_count} resources ({neet_textbooks} textbooks, {neet_papers} question banks)")
        print(f"   JEE: {jee_count} resources ({jee_textbooks} textbooks, {jee_papers} question banks)")
        print(f"   Total: {neet_count + jee_count} resources")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    update_resources()
