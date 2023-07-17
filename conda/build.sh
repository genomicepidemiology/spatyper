#!/bin/bash

mkdir -p ${PREFIX}/bin

chmod +x spatyper.py
cp spatyper.py ${PREFIX}/bin/spatyper.py

# copy script to download database
chmod +x ${RECIPE_DIR}/download-spatyper-db.sh
cp ${RECIPE_DIR}/download-spatyper-db.sh ${PREFIX}/bin/download-spatyper-db.sh

