from flask import Flask, redirect, url_for, jsonify
import secrets
from googleapiclient.discovery import build
from routes.auth import auth_router, load_credentials, save_credentials

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Register the auth router
app.register_blueprint(auth_router, url_prefix='/auth')

@app.route('/test')
def test_api_request():
    """Test API call to list Google Classroom courses."""
    credentials = load_credentials()

    if not credentials:
        return redirect(url_for('auth.authorize'))

    # Refresh credentials if needed
    if not credentials.valid and credentials.expired and credentials.refresh_token:
        credentials.refresh()

    # Call the Classroom API
    service = build("classroom", "v1", credentials=credentials)
    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
        return "No courses found."

    # Save refreshed credentials
    save_credentials(credentials)

    return jsonify(results)

@app.route('/getAllCourses')
def get_courses():
    """Get all available courses from Google Classroom."""
    credentials = load_credentials()

    if not credentials:
        return redirect(url_for('auth.authorize'))

    # Refresh credentials if expired
    if not credentials.valid and credentials.expired and credentials.refresh_token:
        credentials.refresh()

    # Call the Classroom API
    service = build("classroom", "v1", credentials=credentials)
    results = service.courses().list(pageSize=10).execute()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
