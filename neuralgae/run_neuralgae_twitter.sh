#!/bin/bash


NEUHOME="/Users/mike/Desktop/Personal/bots/neuralgae"
BCHOME="/Users/mike/Desktop/Personal/bots/botclient"

export PYTHONPATH="$BCHOME:$PYTHONPATH"

python ${BCHOME}/picturebot.py -d -c ${NEUHOME}/config.yml
