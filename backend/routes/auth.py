from flask import Blueprint, redirect, session, url_for, request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import json
import os

# Define the router for authentication
auth_router = Blueprint('auth', __name__)

#no https, for testing purposes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Define OAuth Scopes
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
]

# File to store credentials
CREDENTIALS_FILE = 'stored_credentials.json'

def save_credentials(credentials):
    """Save user credentials to a JSON file."""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials_to_dict(credentials), f)

def load_credentials():
    """Load user credentials from the JSON file."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_dict = json.load(f)
            return google.oauth2.credentials.Credentials(**creds_dict)
    return None

def credentials_to_dict(credentials):
    """Convert credentials object to a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

@auth_router.route('/authorize')
def authorize():
    """Start the OAuth authorization flow."""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES)

    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    # Store the state to validate the callback
    session['state'] = state
    return redirect(authorization_url)

@auth_router.route('/oauth2callback')
def oauth2callback():
    """Handle the OAuth callback and save credentials."""
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)

    # Get the authorization response
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials
    credentials = flow.credentials
    save_credentials(credentials)

    return "Logged in successfully!"
