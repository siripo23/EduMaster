#!/usr/bin/env python3
"""
Script to add resource files to the database
Usage: python add_resources.py
"""

from app import app
from models import db, Resource

def add_resources():
    """Add resource files to database"""
    
    with app.app_context():
        resources = []
        
        # NEET Past Papers
        neet_papers = [
            ('NEET 2025 Question Paper', 2025, 'NEET_2025.pdf'),
            ('NEET 2024 Question Paper', 2024, 'NEET_2024.pdf'),
            ('NEET 2023 Question Paper', 2023, 'NEET_2023.pdf'),
            ('NEET 2023 Question Paper (Official)', 2023, 'neet_2023_question_paper.pdf'),
            ('NEET 2021 Question Paper', 2021, 'NEET_2021.pdf'),
            ('NEET 2020 Question Paper', 2020, 'NEET_2020.pdf'),
        ]
        
        for title, year, filename in neet_papers:
            resources.append({
                'title': title,
                'resource_type': 'past_paper',
                'subject': 'All Subjects',
                'file_path': f'/static/resources/{filename}',
                'stream': 'NEET',
                'year': year
            })
        
        # JEE Papers (JEE1 to JEE38)
        for i in range(1, 39):
            resources.append({
                'title': f'JEE Question Paper {i}',
                'resource_type': 'past_paper',
                'subject': 'All Subjects',
                'file_path': f'/static/resources/JEE{i}.pdf',
                'stream': 'JEE',
                'year': None  # Year not specified in filename
            })
        
        # JEE Main 2023
        resources.append({
            'title': 'JEE Main 2023 Question Paper',
            'resource_type': 'past_paper',
            'subject': 'All Subjects',
            'file_path': '/static/resources/jee_main_2023_question_paper.pdf',
            'stream': 'JEE',
            'year': 2023
        })
        
        # Add resources to database
        added_count = 0
        skipped_count = 0
        
        for resource_data in resources:
            # Check if resource already exists
            existing = Resource.query.filter_by(
                file_path=resource_data['file_path']
            ).first()
            
            if not existing:
                resource = Resource(**resource_data)
                db.session.add(resource)
                added_count += 1
                print(f"✓ Added: {resource_data['title']}")
            else:
                skipped_count += 1
                print(f"⊘ Skipped (already exists): {resource_data['title']}")
        
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"Resources processed successfully!")
        print(f"✓ Resources added: {added_count}")
        print(f"⊘ Resources skipped: {skipped_count}")
        print(f"📊 Total resources in database: {Resource.query.count()}")
        print(f"{'='*60}")
        
        # Show breakdown by stream
        neet_count = Resource.query.filter_by(stream='NEET').count()
        jee_count = Resource.query.filter_by(stream='JEE').count()
        
        print(f"\n📚 Resources by Stream:")
        print(f"   NEET: {neet_count} resources")
        print(f"   JEE: {jee_count} resources")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    add_resources()
