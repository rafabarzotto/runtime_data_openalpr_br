from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 180
camera.resolution = (1980, 1080)
camera.framerate = 15
camera.start_preview()
sleep(5)
camera.capture('/home/pi/fotos/foto.jpg')
camera.stop_preview()
