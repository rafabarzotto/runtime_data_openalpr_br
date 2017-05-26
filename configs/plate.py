from openalpr import Alpr
import os


alpr = Alpr("br", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(40)
alpr.set_default_region("md")

def reconhece():
	if os.path.exists("/home/ubuntu/Abre.jpg"):
		results = alpr.recognize_file("/home/ubuntu/Abre.jpg")
		lista = []

		i = 0
		for plate in results['results']:
    			i += 1
    			print("   %12s %12s" % ("Plate", "Confidence"))
    			for candidate in plate['candidates']:
        			prefix = "-"
        			if candidate['matches_template']:
            				prefix = "*"

        				print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
					lista.extend([{'placa': candidate['plate'], 'confidencia': candidate['confidence']}])

		#print (lista)
		#print max(lista,key=lambda item:item['confidencia'])
		certo = max(lista,key=lambda item:item['confidencia'])
		#print certo['placa']

		f = open("plate.txt", "w")
		#for item in lista:
		#	f.write("%s;" % item)	
		f.write(certo['placa'])
		f.close()

		# Call when completely done to release memory
		alpr.unload()
		os.remove("/home/ubuntu/Abre.jpg")
	else:
		print "Arquivo nao encontrado"

reconhece()
