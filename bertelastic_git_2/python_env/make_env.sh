#!/bin/sh
sudo apt install -y  python3-pip
sudo pip install -y  pipenv
sudo pipenv pipenv --python 3
sudo pipenv install -r ./requirements.txt
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y libmecab2 libmecab-dev mecab mecab-utils nkf
wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
tar xvzf mecab-ipadic-2.7.0-20070801.tar.gz
nkf --overwrite -Ew mecab-ipadic-2.7.0-20070801/*
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
xz -dkv mecab-ipadic-neologd/seed/*seed*
sudo mv mecab-ipadic-neologd/seed/*.csv mecab-ipadic-2.7.0-20070801/
cd /usr/lib/mecab
sudo ./mecab-dict-index -f utf-8 -t utf-8 -d ~/mecab-ipadic-2.7.0-20070801
sudo chmod a+w /usr/lib/x86_64-linux-gnu
cd /app/mecab-ipadic-2.7.0-20070801
sudo ./configure && make install
sudo chmod a+w /etc/mecabrc
sudo echo 'dicdir=/usr/lib/x86_64-linux-gnu/mecab/dic/ipadic' > /etc/mecabrc
sudo pipenv install mecab-python3