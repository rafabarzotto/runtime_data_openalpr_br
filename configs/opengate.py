#!/usr/bin/python

import beanstalkc
import datetime
import json
import os
import time
import csv


os.system("/usr/bin/alprd & ")
whitelist = ["your plate here"]
beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.watch('alprd')

def opengate():
   print ("Opening gate.")
   os.system("sudo echo -e '\xff\x01\x01' > /dev/ttyUSB0") #on
   time.sleep(1)
   os.system("sudo echo -e '\\xff\\x01\\x00' > /dev/ttyUSB0") #off
   print ("Gate Opened")
   time.sleep(45)
   emptybeanstalk();

def emptybeanstalk():
   print ("Emptying beanstalk.")
   s = beanstalk.stats_tube("alprd")
   ss = s['current-jobs-ready']
   while (ss > 0):
       bos = beanstalk.reserve()
       bos.delete()
       ss -= 1
   beanstalk.watch('alprd')
   print ("Beanstalk emptied.")
   print ("Watching gate.")

def main():
   emptybeanstalk();
   while True:
       job = beanstalk.reserve()
       jobb = job.body
       job.delete()
       d = json.loads(jobb)
       epoch = d['epoch_time']
       #print epoch
       realtime = datetime.datetime.fromtimestamp(epoch / 1e3).strftime('%d-%m-%Y %H:%M:%S')
       #print realtime
       proctime = d['processing_time_ms']
       plate = d['results'][0]['plate']
       confid = d['results'][0]['confidence']
       uuid = d['uuid']
       plates = open('/home/opt/plates.csv', 'a')
       s = (str(realtime) + ", " + str(plate) + ", " + str(confid) + ", " + str(uuid) + "\n")
       plates.write(s)
       plates.close()
       print s
       if plate in whitelist:
           opengate()

if __name__ == "__main__":
   main()
