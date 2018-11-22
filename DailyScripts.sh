#!/bin/sh
# This script runs daily to ingest the event data used in Int01
DATE=`date +%Y%m%d`
HOME_DIR="/home/youview"
SCRIPTS_DIR="$HOME_DIR/scripts/CCO-ingest-scripts/auto-ingests"
LOGGING_DIR="$HOME_DIR/logs"
#Delete the old xml/ folder before running the script
rm -r $HOME_DIR/xml/*
rm -r $SCRIPTS_DIR/xml/*
rm $SCRIPTS_DIR/*.xml
rm $HOME_DIR/*.xml

# Create directories for today's logs
mkdir -p $LOGGING_DIR/Parental/$DATE
mkdir -p $LOGGING_DIR/Parental/$DATE/xml
mkdir -p $LOGGING_DIR/LCN549/$DATE
mkdir -p $LOGGING_DIR/LCN549/$DATE/xml
mkdir -p $LOGGING_DIR/do_ingest/$DATE
mkdir -p $LOGGING_DIR/do_ingest/$DATE/xml
mkdir -p $LOGGING_DIR/Radio/$DATE
mkdir -p $LOGGING_DIR/Radio/$DATE/xml
mkdir -p $LOGGING_DIR/CANTST-10426/$DATE
mkdir -p $LOGGING_DIR/CANTST-10426/$DATE/xml
mkdir -p $LOGGING_DIR/UHD_scripts/$DATE
mkdir -p $LOGGING_DIR/UHD_scripts/$DATE/xml


# Parental Guidance
python $SCRIPTS_DIR/ParentalGuidance.py >> $LOGGING_DIR/Parental/$DATE/Parental.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/Parental/$DATE/

# ParentalG for Sub
python $SCRIPTS_DIR/ParentalGuidanceSub.py >> $LOGGING_DIR/Parental/$DATE/ParentalSub.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/Parental/$DATE/

# ParentalG for Sub
python $SCRIPTS_DIR/ParentalGuidance553.py >> $LOGGING_DIR/Parental/$DATE/ParentalGuidance553.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/Parental/$DATE/

# ParentalG for Sub
python $SCRIPTS_DIR/ParentalGuidance554.py >> $LOGGING_DIR/Parental/$DATE/ParentalGuidance554.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/Parental/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/Parental/$DATE/

# LCN 549
python $SCRIPTS_DIR/LCN549.py >> $LOGGING_DIR/LCN549/$DATE/LCN549.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/LCN549/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/LCN549/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/LCN549/$DATE/

# do_ingest
python $SCRIPTS_DIR/do_ingest.py 6 >> $LOGGING_DIR/do_ingest/$DATE/do_ingest.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/do_ingest/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/do_ingest/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/do_ingest/$DATE/

# Radio
python $SCRIPTS_DIR/Radio_ingest.py >> $LOGGING_DIR/Radio/$DATE/Radio_ingest.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/Radio/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/Radio/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/Radio/$DATE/

#### CANTST-10426 #######
python $SCRIPTS_DIR/CANTST-10426.py >> $LOGGING_DIR/CANTST-10426/$DATE/CANTST-10426.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/CANTST-10426/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/CANTST-10426/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/CANTST-10426/$DATE/

#### UHD script - IPC 570 ###
python $SCRIPTS_DIR/UHD_scripts/UHD_IP_OD.py >> $LOGGING_DIR/UHD_scripts/$DATE/570_UHD_IP_OD.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/UHD_scripts/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/UHD_scripts/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/UHD_scripts/$DATE/

#### UHD script - IPC 571 ###
python $SCRIPTS_DIR/UHD_scripts/571_UHD_IP_no_OD.py >> $LOGGING_DIR/UHD_scripts/$DATE/571_UHD_IP_no_OD.log
mv -f $HOME_DIR/xml/*.xml $LOGGING_DIR/UHD_scripts/$DATE/xml/
mv -f $SCRIPTS_DIR/xml/*.xml $LOGGING_DIR/UHD_scripts/$DATE/xml/
mv -f $HOME_DIR/*.xml $LOGGING_DIR/UHD_scripts/$DATE/


