from openalpr import Alpr
import os
import datetime

alpr = Alpr("br", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(40)
alpr.set_default_region("md")

arq_foto = "/home/pi/fotos/foto.jpg"
dir_saida = "/home/pi/saida/placa.txt"

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
			print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + certo['placa']
	else:
		print "Arquivo nao encontrado"



reconhece()
