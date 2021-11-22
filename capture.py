import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera
from Google import Create_Service #Google.py source code: https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
from googleapiclient.http import MediaFileUpload

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
folder_id = '1-E0rlOk1gInyRbfWzJakXtVKndYcaGkt'

def uploadToServer(image_file): #Uploads image to google drive folder specified above

  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 

  file_names = [image_file]
  file_types = ['image/jpeg']

  for file_name, file_type in zip(file_names, file_types):
    file_metadata = {
      'name': file_name.replace("/home/pi/Documents/GA/captured_img/", ""),
      'parents': [folder_id]
    }

    media = MediaFileUpload(image_file, mimetype=file_type)

    service.files().create(
      body = file_metadata,
      media_body = media,
      fields = 'id'
    ).execute()

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