#! /bin/bash

mkdir tmp
cd tmp
wget https://downloads.cask.co/cdap-sandbox/cdap-sandbox-5.1.2.zip
unzip cdap-sandbox-5.1.2.zip
git lfs clone https://github.com/cdapio/cask-marketplace.git
python ./generate-plugins/main.py ./tmp/cdap-sandbox-5.1.2 ./tmp/cask-marketplace -o plugins_list.json
cp plugins_list.json ../data/en/
