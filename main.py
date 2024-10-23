import os
import io
import time
import requests
import threading
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

COURSE_ID = '723834871032'  # Replace with your actual course ID
SERVICE_ACCOUNT_FILE = '/Users/frankhou/Desktop/googleAPI/serviceKey.json'  # Update this path

# Define scopes for the API
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

# Directory paths
COURSE_MATERIALS_DIR = './course_materials'

def check_existing_file(file_name):
    file_path = os.path.join(COURSE_MATERIALS_DIR, file_name)
    return os.path.isfile(file_path)

def download_file_parallel(service, file_id, file_name):
    try:
        if check_existing_file(file_name):
            print(f"File {file_name} already exists. Skipping download.")
            return

        file_metadata = service.files().get(fileId=file_id, fields='mimeType,size,exportLinks').execute()
        mime_type = file_metadata.get('mimeType')
        file_size = int(file_metadata.get('size', 0))
        export_links = file_metadata.get('exportLinks', {})
        num_threads = 5

        if mime_type.startswith('application/vnd.google-apps'):
            if 'application/pdf' in export_links:
                download_url = export_links['application/pdf']
                file_name = file_name.rsplit('.', 1)[0] + '.pdf'
            else:
                print(f"Unable to export {file_name} to PDF. Skipping download.")
                return
        else:
            download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

        file_path = os.path.join(COURSE_MATERIALS_DIR, file_name)

        def download_chunk(start, end, thread_name):
            headers = {
                'Range': f'bytes={start}-{end}',
                'Authorization': f'Bearer {service._http.credentials.token}'
            }
            response = requests.get(download_url, headers=headers, stream=True)
            response.raise_for_status()
            with open(file_path, 'r+b') as fh:
                fh.seek(start)
                fh.write(response.content)
            print(f"{thread_name} finished downloading bytes {start} to {end}.")

        with open(file_path, 'wb') as f:
            f.write(b'\0' * file_size)

        chunk_size = file_size // num_threads
        threads = []
        for i in range(num_threads):
            start = i * chunk_size
            end = (i+1) * chunk_size - 1 if i < num_threads - 1 else file_size - 1
            thread = threading.Thread(target=download_chunk, args=(start, end, f'Thread-{i+1}'))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print(f"Successfully downloaded {file_name}")
    except Exception as e:
        print(f"Error downloading file {file_name}: {e}")

def fetch_video(service, video_id, file_name):
    try:
        video_metadata = service.files().get(fileId=video_id, fields='mimeType,name').execute()
        mime_type = video_metadata.get('mimeType')

        if mime_type.startswith('video/'):
            request = service.files().get_media(fileId=video_id)
            file_path = os.path.join(COURSE_MATERIALS_DIR, file_name)
            with open(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}% complete for video {file_name}.")
            print(f"Successfully downloaded video {file_path}")
        else:
            print(f"The specified file {file_name} is not a video.")
    except Exception as e:
        print(f"Error fetching video {file_name}: {e}")

def fetch_video_with_error_handling(service, video_id, file_name, max_retries=5):
    for attempt in range(max_retries):
        try:
            fetch_video(service, video_id, file_name)
            return  # Exit if successful
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 403:
                print(f"Insufficient permissions to access video {file_name}.")
                break  # Exit on permissions error
            elif error.response.status_code == 429:
                sleep_time = (2 ** attempt) + (random.random() * 0.1)  # Exponential backoff with jitter
                print(f"Rate limit exceeded. Retrying in {sleep_time:.2f} seconds.")
                time.sleep(sleep_time)
            else:
                print(f"An error occurred while fetching video {file_name}: {error}")
                break  # Exit after handling error
        except Exception as e:
            print(f"Error fetching video {file_name}: {e}")
            break  # Exit on other exceptions

def main():
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
    drive_service = build('drive', 'v3', credentials=creds)

    os.makedirs(COURSE_MATERIALS_DIR, exist_ok=True)

    try:
        coursework_materials = classroom_service.courses().courseWorkMaterials().list(courseId=COURSE_ID).execute()
        
        if 'courseWorkMaterial' not in coursework_materials:
            print("No course materials found.")
        else:
            for material in coursework_materials['courseWorkMaterial']:
                for item in material.get('materials', []):
                    drive_file_info = item.get('driveFile', {}).get('driveFile')
                    if drive_file_info:
                        file_id = drive_file_info.get('id')
                        file_name = drive_file_info.get('title', 'Untitled')
                        if file_id:
                            try:
                                file_metadata = drive_service.files().get(fileId=file_id, fields='mimeType').execute()
                                mime_type = file_metadata.get('mimeType', '')
                                
                                if mime_type.startswith('video/'):
                                    fetch_video_with_error_handling(drive_service, file_id, file_name)
                                else:
                                    download_file_parallel(drive_service, file_id, file_name)
                                
                                time.sleep(1)  # Add a small delay between downloads to avoid rate limiting
                            except Exception as e:
                                print(f"Error processing {file_name}: {e}")
                        else:
                            print("File ID not found.")
                
    except Exception as e:
        print(f'An error occurred while fetching course materials: {e}')

if __name__ == '__main__':
    main()