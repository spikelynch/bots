#!/bin/bash

BHOME="/home/pi/bots"
UHOME="$BHOME/usylessly"

export PYTHONPATH="$BHOME/botclient:$PYTHONPATH"
export TORCH_RNN="/home/pi/torch/torch-rnn"
export TORCH_TH="/home/pi/torch/install/bin/th"

/usr/bin/python3.2 ${UHOME}/usylessly.py -c ${UHOME}/config.yml -e $1  
