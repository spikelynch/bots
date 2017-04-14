#!/bin/bash

BHOME="/Users/mike/Desktop/Personal/bots"
UHOME="$BHOME/usylessly"

export PYTHONPATH="$BHOME/twitterbot:$PYTHONPATH"
export TORCH_RNN="/Users/mike/torch/torch-rnn"
export TORCH_TH="/Users/mike/torch/install/bin/th"

python ${UHOME}/usylessly.py  -d -c ${UHOME}/config.yml -e $1
