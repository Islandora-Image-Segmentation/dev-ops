#!/usr/bin/bash

if [ ! -d venv ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

python src/main.py download 'https://islandnewspapers.ca/islandora' -q cow -l -c 10
python src/main.py prep --issues dir --newspapers dir
vagrant up
vagrant package
vagrant destroy -f
