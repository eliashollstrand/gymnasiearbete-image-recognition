import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera
from Google import Create_Service #Google.py source code: https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
from googleapiclient.http import MediaFileUpload
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920, 1080))

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
all_folder_id = "13wCwokR7xvUYpRPVtb2Gvs58uvJdnZj3"
today_folder_id = "1Iz-7bHUY_n07vpF2HDmw3ZpRQDaVb3yh"
folders = [all_folder_id, today_folder_id]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 

def uploadToServer(image_file): #Uploads image to google drive folder specified above

  file_name = image_file
  file_type = 'image/jpeg'

  items = []
  for folder in folders:
    file_metadata = {
      'name': file_name.replace("/home/pi/Documents/GA/captured_img/", ""),
      'parents': [folder]
    }

    results = service.files().list(fields="nextPageToken, files(id, name, mimeType, size, parents)").execute()
    items = results.get('files', [])

    media = MediaFileUpload(image_file, mimetype=file_type)

    service.files().create(
      body = file_metadata,
      media_body = media,
      fields = 'id'
    ).execute()
  print("Image uploaded to server")
  
  for item in items:
    date_taken = item["name"][:10] # checks first part of string (YYYY-MM-DD)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    if(item["mimeType"] == "image/jpeg"):
      if(item["parents"][0] == today_folder_id and date_taken != today): # delete files from "Today's images" if they aren't from today
        service.files().delete(fileId=item["id"]).execute()
        print("Deleted " + item["name"] + " from Today's images")

def captureImage():
  cam.start()
  image = cam.get_image()
  cam.stop()
  timestr = time.strftime("%Y-%m-%d %H.%M.%S")
  file = "/home/pi/Documents/GA/captured_img/" + timestr
  pygame.image.save(image, file + ".jpg")
  print("Image captured")
  uploadToServer(file + ".jpg")
 
while True:
  i = GPIO.input(GPIO_PIR)
  print(i)

  if i == 1:
    print("Motion detected")
    captureImage()
    time.sleep(1)