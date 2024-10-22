import flask
import requests
import secrets
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os 

#for testing purposes, no need for https
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the Flask app
app = flask.Flask(__name__)
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

SCOPES = ['https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly']


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
    flask.session['credentials'] = credentials_to_dict(credentials)

    print(flask.session['credentials'])

    return "hi"

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}



# Run the server
if __name__ == '__main__':
    app.run(debug=True)
