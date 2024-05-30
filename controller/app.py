from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = r'C:\Users\Sumfl\OneDrive\Documents\GitHub\fyp\service_account.json'
PARENT_FOLDER_ID = "1VuGchHSjYHFoPjbBf8Li4cVybz-sNVIE"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_folder(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    # Get the file name from the file path
    file_name = os.path.basename(file_path)
    
    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID],
    }
    
    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()
    

upload_folder(r"C:\Users\Sumfl\OneDrive\Documents\GitHub\fyp\images\2024-05-30_13-09-57")
