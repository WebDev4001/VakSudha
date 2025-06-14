# Accessibility Learning Platform

## Overview

The Accessibility Learning Platform is a web application designed to help users practice and improve their speech and gesture communication skills. It provides interactive exercises, real-time feedback using AI-powered analysis, and tracks user progress. The platform also offers API endpoints for potential integration with external tools like chatbots.

## Features

*   **User Authentication:** Secure user registration and login system.
*   **Speech Practice:** Allows users to record their speech.
    *   Utilizes OpenAI API for speech analysis, providing scores and constructive feedback.
    *   Live transcription of speech.
*   **Gesture Practice:** Enables users to practice gestures using their webcam.
    *   Uses MediaPipe for real-time gesture detection and visualization.
    *   Feedback on detected gestures.
*   **Progress Tracking:** Users can view their scores and feedback from completed exercises on a personal dashboard.
*   **Interactive Exercises:** A list of predefined speech and gesture exercises with varying difficulty.
*   **API for Chatbot Integration:** Endpoints to fetch exercises and user progress, allowing for potential chatbot interactions.
*   **Custom Error Pages:** User-friendly 404 and 500 error pages.
*   **Enhanced User Interface:** Modern look and feel with smooth animations and transitions for improved interactivity.

## Tech Stack

*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
*   **Database:** SQLite (default), PostgreSQL (configurable)
*   **AI/ML:**
    *   OpenAI API (for speech analysis)
    *   Google MediaPipe (for gesture detection)
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap, Font Awesome
*   **Testing:** Python `unittest` module

## Setup and Installation

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   A virtual environment tool (e.g., `venv`) is highly recommended.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd accessibility-learning-platform
    ```
    *(Replace `<repository_url>` with the actual URL of your repository)*

2.  **Create and Activate a Virtual Environment:**
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    Make sure you have the `requirements.txt` file from the project.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**
    Create a `.env` file in the project root or set these variables directly in your environment.
    *   **`SECRET_KEY` (Required):** Used by Flask for session management and security.
        Generate a strong secret key using:
        ```bash
        python -c "import secrets; print(secrets.token_hex(24))"
        ```
        Example for `.env` file:
        `SECRET_KEY='your_generated_secret_key'`

    *   **`OPENAI_API_KEY` (Required for Speech Analysis):** Your API key for accessing OpenAI services.
        Get this key from your [OpenAI Dashboard](https://platform.openai.com/api-keys).
        Example for `.env` file:
        `OPENAI_API_KEY='sk-your_openai_api_key'`
        *Note: Speech analysis features will not work without this key.*

    *   **`DATABASE_URL` (Optional):** Specifies the database connection string.
        *   Defaults to a local SQLite database: `sqlite:///app.db`
        *   For PostgreSQL, it might look like: `postgresql://username:password@host:port/database_name`
        If you change this, you might need to install additional database drivers (e.g., `psycopg2-binary` for PostgreSQL).

    *If using a `.env` file, ensure your application loads it (e.g., using `python-dotenv` library, which should be in `requirements.txt` if used by the app, or you might need to add it: `pip install python-dotenv` and load it in `app.py`). The current application structure might rely on these being system environment variables if `python-dotenv` is not explicitly used for loading.*

## Running the Application

1.  **Initialize the Database (if not done automatically by the app):**
    The application is configured to create database tables on startup if they don't exist.

2.  **Run the Flask Development Server:**
    Ensure your environment variables are set and your virtual environment is activated.
    The main application script is assumed to be `app.py` or `main.py`. If it's `app.py`:
    ```bash
    python app.py
    ```
    Or, if you have a `main.py` that imports and runs the app:
    ```bash
    python main.py
    ```
    *(Adjust the command based on your main application script name.)*

3.  **Access the Application:**
    Open your web browser and go to:
    `http://127.0.0.1:5000` (or the address shown in your terminal, often `http://0.0.0.0:5000`).

## Running Tests

To run the automated unit tests:

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Navigate to the project root directory.
3.  Execute the following command:
    ```bash
    python -m unittest discover tests
    ```
    Alternatively, you can run a specific test file:
    ```bash
    python tests/test_app.py
    ```

## API Endpoints

The application provides the following API endpoints, primarily for potential chatbot or external tool integration. These endpoints generally require user authentication.

*   `GET /api/exercises`: Retrieves a list of all available practice exercises.
*   `GET /api/user/<user_id>/progress`: Retrieves the progress records for a specific user.
*   `POST /api/save-progress`: Saves a user's progress for an exercise.
*   `POST /api/analyze-speech`: Analyzes provided speech text using OpenAI (requires `OPENAI_API_KEY`).

## Directory Structure (Simplified)

```
.
├── app.py                # Main Flask application file (or main.py)
├── requirements.txt      # Project dependencies
├── static/               # Static assets (CSS, JavaScript, images)
│   ├── css/
│   └── js/
├── templates/            # HTML templates
│   ├── errors/           # Custom error pages (404.html, 500.html)
│   └── ...               # Other HTML files (base.html, index.html, etc.)
├── tests/                # Unit tests
│   ├── __init__.py
│   └── test_app.py
├── utils/                # Utility modules
│   └── openai_helper.py  # OpenAI API related functions
├── models.py             # SQLAlchemy database models
└── README.md             # This file
```

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these general steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them with clear messages.
4.  Ensure your changes pass all tests. Add new tests for new features.
5.  Push your changes to your forked repository.
6.  Create a Pull Request to the main repository.

Please ensure your code adheres to any existing coding style and includes relevant documentation.
