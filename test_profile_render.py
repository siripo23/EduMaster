#!/usr/bin/env python3
"""Test profile template rendering"""

from app import app
from models import db, User, TestAttempt
from flask import render_template_string

with app.app_context():
    # Get user and tests
    user = User.query.first()
    test_history = TestAttempt.query.filter_by(user_id=user.id).all()
    
    print(f"User: {user.name}")
    print(f"Tests: {len(test_history)}")
    
    # Test the calculation
    for test in test_history:
        max_score = test.total_questions * 4
        percentage = (test.score / max_score * 100) if max_score > 0 else 0
        print(f"Test {test.id}: {test.score}/{max_score} = {percentage:.1f}%")
    
    # Try to render a simple version
    template = """
    {% for test in test_history %}
    <tr>
        <td>{{ test.score }}/{{ test.total_questions * 4 }}</td>
        <td>
            {% set max_score = test.total_questions * 4 %}
            {% set percentage = ((test.score / max_score * 100) if max_score > 0 else 0) %}
            {{ "%.1f"|format(percentage) }}%
        </td>
    </tr>
    {% endfor %}
    """
    
    try:
        result = render_template_string(template, test_history=test_history)
        print("\nTemplate rendered successfully!")
        print(result)
    except Exception as e:
        print(f"\nTemplate error: {e}")
        import traceback
        traceback.print_exc()
