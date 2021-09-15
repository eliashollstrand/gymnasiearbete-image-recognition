import RPi.GPIO as GPIO
import time
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)
 
while True:
  i = GPIO.input(GPIO_PIR)
  if i==0:
    print("No motion detected", i)
    time.sleep(1)
  elif i==1:
    print("Motion detected", i)
    time.sleep(1)