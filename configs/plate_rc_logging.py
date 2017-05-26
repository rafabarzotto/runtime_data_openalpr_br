from openalpr import Alpr
import os
import glob
import datetime
import logging

alpr = Alpr("br", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(40)
alpr.set_default_region("md")

logging.basicConfig(filename='/home/opt/out/plate_log.log',level=logging.DEBUG)
dataAtual = datetime.datetime.now().strftime("%d-%m-%Y")
list_of_files = glob.glob('/home/opt/ftp/192.168.255.72/' + dataAtual + '/*') # * means all if need specific format then *.csv
if not list_of_files:
	print "Diretorio Vazio"
	arq_foto = ""
	dir_saida = ""
else:
	arq_foto = max(list_of_files, key=os.path.getctime)
	dir_saida = "/home/opt/out/placa.txt"

#print list_of_files

def reconhece():
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
			logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Nao Reconheceu')
			print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Nao Reconheceu'
		else:
			#print max(lista,key=lambda item:item['confidencia'])
			certo = max(lista,key=lambda item:item['confidencia'])
			print certo['placa']

			f = open(dir_saida, "w")
			#for item in lista:
				#f.write("%s;" % item)	
			f.write(certo['placa'])
			f.close()

			# Call when completely done to release memory
			alpr.unload()
			os.remove(arq_foto)
			logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + certo['placa'])
			print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + certo['placa']
			
	else:
		logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Arquivo nao encontrado')
		print "Arquivo nao encontrado"



reconhece()
