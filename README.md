# Accessibility Learning Platform

## Overview

The Accessibility Learning Platform is a web application designed to help users practice and improve their speech and gesture communication skills. It provides interactive exercises, real-time feedback using AI-powered analysis, and tracks user progress. The platform also offers API endpoints for potential integration with external tools like chatbots.

## Features

The Accessibility Learning Platform offers a rich set of features designed for an effective and engaging learning experience:

**Core Practice Functionalities:**
*   **Speech Practice:**
    *   Record audio directly in the browser.
    *   See live transcription of your speech.
    *   Receive AI-powered analysis from OpenAI, including a score, detailed feedback, and areas for improvement.
*   **Gesture Practice:**
    *   Utilize your webcam for real-time gesture recognition powered by MediaPipe.
    *   Visual feedback with hand landmark overlays.
    *   Basic analysis of performed gestures.
*   **Interactive Exercises:** Access a list of predefined speech and gesture exercises with varying difficulty levels.

**User Experience & Interface:**
*   **Personalized Dashboard:**
    *   Track your overall progress for both speech and gesture exercises.
    *   View average scores and the number of completed exercises.
    *   Review a log of recent activities, including scores and specific feedback for each completed session.
    *   Get recommendations for further practice.
*   **Modern & Responsive UI:**
    *   Clean, intuitive interface with a dark theme for better visual comfort.
    *   Responsive design adapting to desktops, tablets, and mobile devices.
    *   Smooth animations, transitions, and Font Awesome icons enhance interactivity and visual appeal.
*   **User-Friendly Error Handling:** Custom pages for common errors (e.g., Page Not Found, Server Error) to guide users.

**Account Management & Data:**
*   **Secure User Authentication:** Reliable login and logout functionality to protect user data and progress.
*   **Persistent Progress Tracking:** All practice scores and feedback are saved, allowing users to monitor their improvement over time.

**Extensibility & Technical Foundation:**
*   **API for External Integration:** RESTful API endpoints (e.g., `/api/exercises`, `/api/user/<id>/progress`, `/api/analyze-speech`) available for integrating with chatbots or other external tools (requires authentication).
*   **Robust Backend:** Built with Python, Flask, and SQLAlchemy, ensuring a stable and maintainable platform.
*   **Configurable Setup:** Supports SQLite by default and can be configured for PostgreSQL. Clear guidance on environment variable setup for API keys and application settings.
*   **Tested Reliability:** Includes a suite of unit tests to ensure core functionalities work as expected.

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

    *Note on `.env` files: This application does not automatically load environment variables from a `.env` file (e.g., using `python-dotenv`). If you choose to use a `.env` file, you must ensure it is loaded by your environment or by modifying the application to include a library like `python-dotenv`.*

## Running the Application

1.  **Initialize the Database:**
    The application is configured to create database tables on startup if they don't exist, so this step is typically automatic.

2.  **Run the Flask Development Server:**
    Ensure your environment variables are set (as system environment variables or loaded via your preferred method if using `.env` files) and your virtual environment is activated.
    To run the application, use:
    ```bash
    python main.py
    ```
    This script is configured to run the Flask development server. Alternatively, if `main.py` is not used, you might run `python app.py` directly if `app.run()` is called within it.

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
*   `GET /api/user/<user_id>/progress`: Retrieves the progress records for the specified `user_id`.
*   `POST /api/save-progress`: Saves a user's progress for an exercise.
*   `POST /api/analyze-speech`: Analyzes provided speech text using OpenAI (requires `OPENAI_API_KEY`).

## Directory Structure

The project is organized as follows:

```
.
├── .replit                 # Configuration for Replit environment (if used)
├── app.py                  # Main Flask application file: defines routes, app logic.
├── main.py                 # Entry point to run the Flask application.
├── models.py               # SQLAlchemy database models (User, Practice, Progress).
├── requirements.txt        # Python package dependencies for the project.
├── instance/               # Instance-specific data, not version controlled by default.
│   └── app.db              # SQLite database file (default setup).
├── static/                 # Static assets served directly to the client.
│   ├── css/
│   │   └── custom.css      # Custom stylesheets for the application.
│   └── js/
│       ├── app.js          # General frontend JavaScript (e.g., event listeners, UI interactions).
│       ├── gesture.js      # JavaScript for gesture detection using MediaPipe.
│       └── speech.js       # JavaScript for speech recognition and handling.
├── templates/              # HTML templates rendered by Flask.
│   ├── base.html           # Base template with common layout (navbar, footer).
│   ├── dashboard.html      # User dashboard page.
│   ├── index.html          # Homepage / Login page.
│   ├── practice.html       # Page for speech and gesture practice exercises.
│   └── errors/             # Custom error page templates.
│       ├── 404.html        # Template for "Page Not Found" errors.
│       └── 500.html        # Template for "Internal Server Error" errors.
├── tests/                  # Contains all unit tests for the application.
│   ├── __init__.py         # Makes 'tests' a Python package.
│   └── test_app.py         # Main file for application unit tests.
├── utils/                  # Utility modules and helper functions.
│   └── openai_helper.py    # Helper functions for interacting with the OpenAI API.
├── pyproject.toml          # Python project configuration (e.g., for build systems, linters).
├── replit.nix              # Configuration for Replit's Nix environment (if used).
├── uv.lock                 # Lock file for `uv` package manager (if used).
└── README.md               # This file.
```
*Note: `__pycache__/`, `generated-icon.png`, and other similar files are typically not included in the primary project structure documentation as they are auto-generated or artifacts.*

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these general steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them with clear messages.
4.  Ensure your changes pass all tests. Add new tests for new features.
5.  Push your changes to your forked repository.
6.  Create a Pull Request to the main repository.

Please ensure your code adheres to any existing coding style and includes relevant documentation.
