from openalpr import Alpr
import os
import glob
import datetime
import time
import cv2
import urllib
import numpy as np

alpr = Alpr("br", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(40)
alpr.set_default_region("md")

dataAtual = datetime.datetime.now().strftime("%d-%m-%Y")

def take():
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
			print('File Save Success - Wait 10 seconds')
			time.sleep(10)
			reconhece()
			break

def reconhece():
	list_of_files = glob.glob('/home/pi/img/*') # * means all if need specific format then *.csv
	if not list_of_files:
		print "Diretorio Vazio"
		arq_foto = ""
		dir_saida = ""
	else:
		arq_foto = max(list_of_files, key=os.path.getctime)
		dir_saida = "/home/pi/out/"
		#print list_of_files
		
		if os.path.exists(arq_foto):
			results = alpr.recognize_file(arq_foto)
			lista = []

			i = 0
			for plate in results['results']:
					i += 1
					#print("   %12s %12s" % ("Plate", "Confidence"))
					for candidate in plate['candidates']:
						prefix = "-"
						if candidate['matches_template']:
							prefix = "*"
							#print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
							lista.extend([{'placa': candidate['plate'], 'confidencia': candidate['confidence']}])

			if not lista:
				# Call when completely done to release memory
				alpr.unload()
				os.remove(arq_foto)
				plates = open('/home/pi/out/plate_log.csv', 'a')
				s = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + ", " + 'Nao Reconheceu' + "\n")
				plates.write(s)
				plates.close()
				print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Nao Reconheceu'
			else:
				#print max(lista,key=lambda item:item['confidencia'])
				certo = max(lista,key=lambda item:item['confidencia'])
				print certo['placa']

				f = open(dir_saida + certo['placa'] + '.txt', "w")
				#for item in lista:
					#f.write("%s;" % item)
				f.write(certo['placa'])
				f.close()

				# Call when completely done to release memory
				alpr.unload()
				os.remove(arq_foto)
				plates = open('/home/pi/out/plate_log.csv', 'a')
				s = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + ", " + certo['placa'] + '\n')
				plates.write(s)
				plates.close()
				print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + certo['placa']

		else:
			plates = open('/home/pi/out/plate_log.csv', 'a')
			s = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + ", " + 'Arquivo nao encontrado' + "\n")
			plates.write(s)
			plates.close()
			print "Arquivo nao encontrado"


take()

