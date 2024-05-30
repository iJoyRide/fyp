from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os
import mimetypes

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = (
    r"C:\Users\Sumfl\OneDrive\Documents\GitHub\fyp\service_account.json"
)
PARENT_FOLDER_ID = "1VuGchHSjYHFoPjbBf8Li4cVybz-sNVIE"


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return creds


def create_folder(folder_name, parent_folder_id=None):
    """Create a folder in Google Drive and return its ID."""
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    folder_metadata = {
        "name": folder_name,
        "parents": [parent_folder_id] if parent_folder_id else [],
        "mimeType": "application/vnd.google-apps.folder",
    }

    folder = service.files().create(body=folder_metadata, fields="id").execute()

    print(f'Created Folder ID: {folder["id"]}')
    return folder["id"]


def upload_folder_contents(folder_path, parent_folder_id):
    """Upload a folder and its contents to Google Drive."""
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subfolder_id = create_folder(item, parent_folder_id)
            upload_folder_contents(item_path, subfolder_id)
        else:
            upload_file(item_path, parent_folder_id)


def upload_file(file_path, parent_folder_id):
    """Upload a file to Google Drive."""
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    # Get the file name from the file path
    file_name = os.path.basename(file_path)

    file_metadata = {
        "name": file_name,
        "parents": [parent_folder_id],
    }

    # Determine MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    file_metadata["mimeType"] = mime_type

    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    print(f'Uploaded File ID: {file["id"]}')
    return file["id"]


if __name__ == "__main__":
    # Example usage:

    # Upload subfolders and their contents to the parent folder
    upload_folder_contents(
        r"C:\Users\Sumfl\OneDrive\Documents\GitHub\fyp\images", PARENT_FOLDER_ID
    )
