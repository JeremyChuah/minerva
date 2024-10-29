import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def fetch_courses(service):
    courses = service.courses().list().execute()
    course_list = [(course['id'], course['name']) for course in courses.get('courses', [])]
    return course_list

def fetch_course_id_from_classroom():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    classroom_service = build('classroom', 'v1', credentials=creds)
    course_list = fetch_courses(classroom_service)
    
    print('Available Courses:')
    for course_id, course_name in course_list:
        print(f'ID: {course_id}, Name: {course_name}')

if __name__ == '__main__':
    fetch_course_id_from_classroom()
