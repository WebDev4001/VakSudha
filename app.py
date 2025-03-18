import os
import logging
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

# Import routes after app initialization
from models import User, Practice, Progress

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password.', 'danger')

    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    progress = Progress.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, progress=progress)

@app.route('/practice')
@login_required
def practice():
    exercises = Practice.query.all()
    return render_template('practice.html', exercises=exercises)

@app.route('/api/analyze-speech', methods=['POST'])
@login_required
def analyze_speech():
    from utils.openai_helper import analyze_speech_content

    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        analysis = analyze_speech_content(text)
        return jsonify(analysis)
    except Exception as e:
        logging.error(f"Speech analysis error: {str(e)}")
        return jsonify({'error': 'Speech analysis failed'}), 500

@app.route('/api/save-progress', methods=['POST'])
@login_required
def save_progress():
    try:
        data = request.json
        progress = Progress(
            user_id=current_user.id,
            exercise_id=data['exercise_id'],
            score=data['score'],
            feedback=data['feedback']
        )
        db.session.add(progress)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error saving progress: {str(e)}")
        return jsonify({'error': 'Failed to save progress'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logging.error(f"Internal server error: {str(error)}")
    return render_template('index.html'), 500

# Create database tables
with app.app_context():
    db.create_all()