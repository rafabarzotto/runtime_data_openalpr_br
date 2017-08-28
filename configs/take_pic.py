import cv2
import urllib
import numpy as np
import os

#url = 'http://177.155.135.73/cgi-bin/snapshot.cgi'
url = 'http://192.168.250.98:81/video.mjpg'
stream=urllib.urlopen(url)
bytes=''
condicao = True
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imwrite('/home/pi/img/i.jpg',i)
        #if cv2.waitKey(1) ==27:
	if os.path.exists('/home/pi/img/i.jpg'):
           condicao = False
           break
