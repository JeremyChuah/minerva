import google.oauth2.credentials
import google_auth_oauthlib.flow
import json
import os

#no https, for testing purposes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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