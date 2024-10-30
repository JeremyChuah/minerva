from flask import Flask, redirect, url_for, jsonify
import secrets
from googleapiclient.discovery import build
from routes.auth import auth_router, load_credentials, save_credentials
from routes.course import fetch_materials, fetch_courses

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

    #call service
    all_courses = fetch_courses(credentials)
    id = all_courses['courses'][0]['id']
    materials = fetch_materials(id, credentials)
    print(materials)

    return "hi"

if __name__ == '__main__':
    app.run(debug=True)
