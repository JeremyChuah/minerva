import flask
import requests
import secrets
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build
import os
import json

# For testing purposes, no need for HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the Flask app
app = flask.Flask(__name__)
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
]

# File path to store the credentials
CREDENTIALS_FILE = 'stored_credentials.json'


def save_credentials(credentials):
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials_to_dict(credentials), f)


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_dict = json.load(f)
            return google.oauth2.credentials.Credentials(**creds_dict)
    return None


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    save_credentials(credentials)

    return "logged in";


@app.route('/test')
def test_api_request():

    credentials = load_credentials()

    if not credentials:
        return flask.redirect(flask.url_for('authorize'))

    if not credentials.valid and credentials.expired and credentials.refresh_token:
        credentials.refresh(requests.Request())

    service = build("classroom", "v1", credentials=credentials)
    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
        print("No courses found.")
        return "No courses found."
    
    print("Courses:")
    for course in courses:
        print(course["name"])

    save_credentials(credentials)

    return flask.jsonify(**results)


@app.route('/getAllCourses')
def get_courses():
    # Load stored credentials
    credentials = load_credentials()

    if not credentials:
        return flask.redirect(flask.url_for('authorize'))
    
    if not credentials.valid and credentials.expired and credentials.refresh_token:
        credentials.refresh(requests.Request())

    service = build("classroom", "v1", credentials=credentials)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
        return "No courses found."

    return flask.jsonify(**results)


# Run the server
if __name__ == '__main__':
    app.run(debug=True)
