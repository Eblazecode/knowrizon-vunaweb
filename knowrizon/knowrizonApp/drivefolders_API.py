import os
import  json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.shortcuts import render

# COMPUTER SCIENCE CATEGORY MAPPING TO DRIVE FOLDERS; BOOKS CATEGORIES: folder ids
COMPUTER_SCI_DEPT_CATEGORY_TO_FOLDER = {
    "algorithms": "1V7NViMHyErE0DHnVkupfMYkEAGzmIZND",
    "artificial_intelligence": "folder_id_ai",
    "computer_networks": "folder_id_networks",
    "computer_programming": "folder_id_programming",
    "computer_security": "folder_id_security",
    "data_science": "folder_id_data_science",
    "database_management": "folder_id_database",
    "distributed_systems": "folder_id_distributed_systems",
    "machine_learning": "folder_id_machine_learning",
    "operating_systems": "folder_id_os",
    "software_engineering": "folder_id_software_engineering",
    "web_development": "folder_id_web_dev",
    "quantum_computing": "folder_id_quantum_computing",
    "cloud_computing": "folder_id_cloud_computing",
    "blockchain": "folder_id_blockchain",
    "big_data": "folder_id_big_data",
    "iot": "folder_id_iot",
    "cyber_security": "folder_id_cyber_security",
    "mobile_application": "folder_id_mobile_app",
    "robotics": "folder_id_robotics",
    "data_structures": "folder_id_data_structures",
    "computer_graphics": "folder_id_graphics",
    "optimization": "folder_id_optimization",
    "computational_mathematics": "folder_id_computational_mathematics",
    "computer_vision": "folder_id_computer_vision",
}

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'media/config/service_account_API.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


def view_comp_sci_books(request, category):
    # Get the folder ID for the category
    folder_id = COMPUTER_SCI_DEPT_CATEGORY_TO_FOLDER.get(category)

    # Debugging: Print category and folder ID
    print("Requested Category:", category)
    print("Mapped Folder ID:", folder_id)

    # Check if folder ID exists
    if not folder_id:
        return render(request, 'error.html', {"message": "Category not found"})

    # Fetch files from the folder
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        fields="files(id, name, webViewLink)"
    ).execute()

    # Get the list of books
    books = results.get('files', [])

    # Debugging: Print the fetched books
    print("Fetched Books:", books)

    # Render the template
    return render(request, 'books/comp_sci_books.html', {"books": books, "category": category})
