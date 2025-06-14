import os
import sys
import unittest
import json
from unittest.mock import patch

# Adjust path to import app and models
# Assuming app.py and models.py are in the parent directory of 'tests'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Practice, Progress
from werkzeug.security import generate_password_hash

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # Flask-Login requires a secret key for session management
        app.config['SECRET_KEY'] = 'test_secret_key_for_testing'

        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Helper method to create a user
    def _create_user(self, username="testuser", email="test@example.com", password="password"):
        with app.app_context():
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return user

    # Helper method to log in a user
    def _login(self, email="test@example.com", password="password"):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    # --- Test Cases Will Be Added Below ---

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Accessibility Learning Platform", response.data)

    def test_login_logout(self):
        # Create a user
        self._create_user(email="login@example.com", password="testpassword")

        # Test successful login
        response = self._login(email="login@example.com", password="testpassword")
        self.assertEqual(response.status_code, 200) # Assuming redirect to dashboard is 200
        self.assertIn(b"Logged in successfully.", response.data) # Flash message
        self.assertIn(b"Dashboard", response.data) # Should be on dashboard

        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Assuming redirect to index
        self.assertIn(b"Logged out successfully.", response.data)
        self.assertIn(b"Login", response.data) # Should see login button again on index

        # Test login with invalid credentials
        response = self._login(email="login@example.com", password="wrongpassword")
        self.assertEqual(response.status_code, 200) # Login page itself
        self.assertIn(b"Invalid email or password.", response.data)
        # Check that we are on the index page (where login form is)
        self.assertIn(b"Login with Email", response.data)


    def test_protected_route_unauthorized(self):
        # Try to access /dashboard without logging in
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should be redirected to index page (which contains the login form)
        # as per current app.py login route for GET requests
        self.assertIn(b"Login with Email", response.data)
        self.assertNotIn(b"Dashboard", response.data)

    def test_dashboard_access_authorized(self):
        self._create_user(email="dash@example.com", password="testpassword")
        self._login(email="dash@example.com", password="testpassword")

        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)
        self.assertIn(b"dash@example.com", response.data) # Check if user info is displayed

    # Helper method to create a practice exercise
    def _create_practice_exercise(self, title="Test Exercise", description="Test Desc", type="speech", difficulty="easy"):
        with app.app_context():
            exercise = Practice(
                title=title,
                description=description,
                type=type,
                difficulty=difficulty
            )
            db.session.add(exercise)
            db.session.commit()
            return exercise

    def test_api_get_exercises_unauthorized(self):
        response = self.client.get('/api/exercises', follow_redirects=True)
        # Flask-Login redirects to login_view, which is /login
        # /login route redirects to /index for GET.
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login with Email", response.data) # Should be on login/index page

    def test_api_get_exercises_authorized(self):
        self._create_user(email="apiuser@example.com", password="password")
        self._login(email="apiuser@example.com", password="password")

        exercise1 = self._create_practice_exercise(title="Exercise 1")

        response = self.client.get('/api/exercises')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Exercise 1")

    def test_api_save_progress(self):
        user = self._create_user(email="progressuser@example.com", password="password")
        self._login(email="progressuser@example.com", password="password")
        exercise = self._create_practice_exercise(title="Progress Exercise")

        progress_data = {
            'exercise_id': exercise.id,
            'score': 85.5,
            'feedback': 'Good job!'
        }
        response = self.client.post('/api/save-progress', json=progress_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        with app.app_context():
            progress_record = Progress.query.filter_by(user_id=user.id, exercise_id=exercise.id).first()
            self.assertIsNotNone(progress_record)
            self.assertEqual(progress_record.score, 85.5)

    def test_api_get_user_progress(self):
        user = self._create_user(email="getprogress@example.com", password="password")
        self._login(email="getprogress@example.com", password="password")
        exercise = self._create_practice_exercise(title="My Progress Exercise")

        with app.app_context():
            prog = Progress(user_id=user.id, exercise_id=exercise.id, score=90, feedback="Great!")
            db.session.add(prog)
            db.session.commit()

        response = self.client.get(f'/api/user/{user.id}/progress')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['exercise_id'], exercise.id)
        self.assertEqual(data[0]['exercise_title'], "My Progress Exercise")
        self.assertEqual(data[0]['score'], 90)

    def test_api_get_user_progress_unauthorized_other_user(self):
        user1 = self._create_user(email="user1@example.com", password="password")
        user2 = self._create_user(email="user2@example.com", username="user2", password="password")
        self._login(email="user1@example.com", password="password") # Logged in as user1

        response = self.client.get(f'/api/user/{user2.id}/progress')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unauthorized access to progress data.')

    def test_api_get_user_progress_user_not_found(self):
        self._create_user(email="exists@example.com", password="password")
        self._login(email="exists@example.com", password="password")

        non_existent_user_id = 99999
        response = self.client.get(f'/api/user/{non_existent_user_id}/progress')
        self.assertEqual(response.status_code, 404) # Or 403 if current_user.id != non_existent_user_id is hit first
        data = json.loads(response.data)
        self.assertIn('error', data)
        # The actual error message depends on which check is hit first in app.py
        # If current_user.id (e.g. 1) != 99999, it's 403.
        # If we somehow pass that and User.query.get(99999) is None, it's 404.
        # Given current_user.id will not be 99999, it should be 403.
        # Let's re-verify the logic in app.py:
        # 1. if current_user.id != user_id: -> 403
        # 2. user = User.query.get(user_id); if not user: -> 404
        # So, if user_id is non-existent, current_user.id (e.g. 1) will not equal user_id (99999).
        # Thus, it should be a 403.
        # However, the intention of the test is for "user not found".
        # The current structure of the endpoint makes the "user not found" (404) only reachable
        # if current_user.id == user_id, but that user_id doesn't exist (e.g. user deleted after login).
        # For a truly non-existent user_id requested by an authenticated user, it will be 403.
        # This is an acceptable behavior for security (don't reveal if user exists).
        # Let's test for 403 in this scenario.
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['error'], 'Unauthorized access to progress data.')

    @patch('app.analyze_speech_content') # Mock the function directly as imported in app.py
    def test_api_analyze_speech_mocked(self, mock_analyze_speech):
        # Configure the mock
        mock_analyze_speech.return_value = {
            "score": 95.0,
            "feedback": "Mocked excellent pronunciation!",
            "improvements": ["Keep it up!"]
        }

        # Login a user
        self._create_user(email="speechuser@example.com", password="password")
        self._login(email="speechuser@example.com", password="password")

        # Test successful analysis
        speech_data = {'text': 'Hello world, this is a test.'}
        response = self.client.post('/api/analyze-speech', json=speech_data)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 95.0)
        self.assertEqual(data['feedback'], "Mocked excellent pronunciation!")
        mock_analyze_speech.assert_called_once_with('Hello world, this is a test.')

        # Reset mock for the next call if needed, or ensure it wasn't called again if not expected
        mock_analyze_speech.reset_mock()

        # Test with no text provided
        response = self.client.post('/api/analyze-speech', json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No text provided')
        mock_analyze_speech.assert_not_called() # Ensure it wasn't called with empty text

    @patch('app.analyze_speech_content')
    def test_api_analyze_speech_mocked_failure(self, mock_analyze_speech):
        # Configure the mock to raise an exception
        mock_analyze_speech.side_effect = Exception("Mocked OpenAI API failure")

        # Login a user
        self._create_user(email="speechfail@example.com", password="password")
        self._login(email="speechfail@example.com", password="password")

        speech_data = {'text': 'This will fail.'}
        response = self.client.post('/api/analyze-speech', json=speech_data)

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Speech analysis failed')
        mock_analyze_speech.assert_called_once_with('This will fail.')


if __name__ == '__main__':
    unittest.main()
