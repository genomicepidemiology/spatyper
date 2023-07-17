#!/usr/bin/env bash

echo "Downloading lastest version of the spatyper database to current directory..."

mkdir spatyper_db
cd spatyper_db

wget https://bitbucket.org/genomicepidemiology/spatyper_db/get/master.tar.gz
tar -xvf master.tar.gz --strip-components 1

echo "Installing the spatyper database with KMA"
python INSTALL.py

echo "The spatyper database has been downloaded and installed."

exit 0
