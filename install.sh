#!/bin/bash
cd $(dirname "$0") 

virtualenv env
source env/bin/activate

pip install -r requirements.txt

git clone git@github.com:toshima/generalsio.git 
