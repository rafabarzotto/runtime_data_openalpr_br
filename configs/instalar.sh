#!/bin/sh

#check privileges
if [ `id -u` -ne 0 ]; then
  echo "É preciso rodar com sudo"
  exit 1
fi

DIR=$(pwd)

sudo mv /usr/share/openalpr/runtime_data /usr/share/openalpr/runtime_data_old
sudo mv /etc/openalpr/alprd.conf /etc/openalpr/alprd.conf.bak

sudo cp alprd.conf /etc/openalpr/

sudo mkdir /usr/local/bin/plateservice
sudo cp plateservice.py /usr/local/bin/plateservice/
sudo cp plateservice.sh /etc/init.d/plateservice

sudo chmod 755 /usr/local/bin/plateservice/plateservice.py
sudo chmod 755 /etc/init.d/plateservice

cd ..

sudo cp -r runtime_data /usr/share/openalpr/

cd

sudo mkdir out
sudo mkdir fotos

sudo update-rc.d -f alprd remove
sudo update-rc.d -f openalprd-daemon remove
sudo update-rc.d plateservice defaults

echo "OK"