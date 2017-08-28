import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.OUT)

try:
    while (True):
        if(GPIO.input(21) == 1):
            print("Sensor de alinhamento ok capturar placa")
            GPIO.output(20, GPIO.HIGH)
        else:
            print("LOW")
            GPIO.output(20, GPIO.LOW)
	    subprocess.call('python /home/pi/take_recognize.py', shell=True)
	    time.sleep(30)
except KeyboardInterrupt:
    GPIO.clenup()
    print("FIM")  
