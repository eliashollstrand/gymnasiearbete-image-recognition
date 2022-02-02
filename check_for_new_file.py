from Google import Create_Service
from detection import detect

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
folder_id = "1Iz-7bHUY_n07vpF2HDmw3ZpRQDaVb3yh"

all_folder_id = "13wCwokR7xvUYpRPVtb2Gvs58uvJdnZj3"
today_folder_id = "1Iz-7bHUY_n07vpF2HDmw3ZpRQDaVb3yh"
folders = [all_folder_id, today_folder_id]

files = []

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 
results = service.files().list(fields="nextPageToken, files(id, name, mimeType, size, parents)").execute()
items = results.get('files', [])

for item in items:
    files.append(item)

print("Files loaded")



while(True):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 
    results = service.files().list(fields="nextPageToken, files(id, name, mimeType, size, parents)").execute()
    items = results.get('files', [])

    for item in items:
        if(item not in files):
            print("New file added: " + item["name"])
            print("Running detection on " + item["name"] + "...")
            detect(item)
            files.append(item)