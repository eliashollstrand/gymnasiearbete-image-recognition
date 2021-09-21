import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera
from ftplib import FTP

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920, 1080))

ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('192.168.50.3', 21) 
ftp.login('user','1234')
ftp.set_pasv(False)
print("Connected to FTP Server successfully")

def uploadToServer(image_file):
  with open("/home/pi/Documents/GA/captured_img/" + image_file + ".jpg", "rb") as file:
    ftp.storbinary(f"STOR {image_file}.jpg", file)
    print("Image sent successfully to server")

def captureImage():
  cam.start()
  image = cam.get_image()
  cam.stop()
  timestr = time.strftime("%Y%m%d-%H-%M-%S")
  file = "/home/pi/Documents/GA/captured_img/" + timestr
  pygame.image.save(image, file + ".jpg")
  print("Image captured")
  uploadToServer(timestr)
 
while True:
  i = GPIO.input(GPIO_PIR)

  if i == 1:
    print("Motion detected")
    captureImage()
    time.sleep(1)