from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly'
]

def fetch_courses(credentials):
    service = build("classroom", "v1", credentials=credentials)
    courses = service.courses().list().execute()
    return courses

def fetch_materials(course_id, credentials):
    service = build("classroom", "v1", credentials=credentials)
    course_materials = service.courses().courseWorkMaterials().list(courseId=course_id).execute()
    return course_materials

