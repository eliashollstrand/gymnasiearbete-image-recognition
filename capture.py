import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera

 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(1920, 1080))

def captureImage():
  cam.start()
  image = cam.get_image()
  cam.stop()
  timestr = time.strftime("%Y%m%d-%H:%M:%S")
  pygame.image.save(image, "/home/pi/Documents/GA/captured_img/" + timestr)
  print("Image taken")
 
while True:
  i = GPIO.input(GPIO_PIR)

  if i==1:
    print("Motion detected", i)
    captureImage()
    time.sleep(1)