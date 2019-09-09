import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
sensor = 20

GPIO.setup(sensor, GPIO.IN)
print("Settle")
time.sleep(2)
print("Detecting Motion")

while True:
    if GPIO.input(sensor):
        print("Motion Detected")
        time.sleep(2)
    else:
        print("finding...")
    time.sleep(2)
