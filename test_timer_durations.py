"""
Test script to verify timer durations are correct
"""
from app import app
from flask import session
from models import db, User

def test_timer_durations():
    """Test that all test types have correct durations"""
    with app.app_context():
        with app.test_client() as client:
            print("\n" + "="*60)
            print("Testing Timer Durations")
            print("="*60)
            
            # Create a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database. Please create a user first.")
                return
            
            # Test initial test duration
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
            
            print("\n1. Initial Test:")
            response = client.get('/test/start/initial')
            if b'60' in response.data:
                print("   ✅ Duration: 60 minutes")
            else:
                print("   ❌ Duration not found or incorrect")
            
            print("\n2. Adaptive Test:")
            response = client.get('/test/start/adaptive')
            if b'30' in response.data:
                print("   ✅ Duration: 30 minutes")
            else:
                print("   ❌ Duration not found or incorrect")
                # Check what duration is shown
                if b'90' in response.data:
                    print("   ⚠️  Shows 90 minutes (should be 30)")
            
            print("\n3. Full Paper Test:")
            response = client.get('/test/start/full_paper')
            if b'180' in response.data:
                print("   ✅ Duration: 180 minutes (3 hours)")
            else:
                print("   ❌ Duration not found or incorrect")
            
            print("\n4. Subject Test (Physics):")
            response = client.get('/test/start/subject_Physics')
            if b'45' in response.data:
                print("   ✅ Duration: 45 minutes")
            else:
                print("   ❌ Duration not found or incorrect")
            
            print("\n" + "="*60)
            print("Timer Duration Test Summary")
            print("="*60)
            print("\nExpected Durations:")
            print("  - Initial Test: 60 minutes")
            print("  - Adaptive Test: 30 minutes ⭐")
            print("  - Full Paper: 180 minutes (3 hours) ⭐")
            print("  - Subject Test: 45 minutes")
            print("\n⭐ = Recently updated")
            print("="*60 + "\n")

if __name__ == '__main__':
    test_timer_durations()
