#!/bin/bash

DATE=`date +%d-%m-%Y`
LOG_DIR=/home/opt/out/

echo " ----- Renomear ----- "
mv $LOG_DIR/plate_log.log $LOG_DIR/logs/plate_log_$DATE.log
