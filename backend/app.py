from flask import Flask, redirect, url_for, jsonify
import secrets
from googleapiclient.discovery import build
from routes.auth import auth_router
from routes.course import course_router

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Register the auth router
app.register_blueprint(auth_router, url_prefix='/auth')
app.register_blueprint(course_router, url_prefix='/courses')

if __name__ == '__main__':
    app.run(debug=True)
