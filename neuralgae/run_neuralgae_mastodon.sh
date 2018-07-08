#!/bin/bash


NEUHOME="/home/mikelynch/bots/neuralgae"
BCHOME="/home/mikelynch/bots/botclient"

export PYTHONPATH="$BCHOME:$PYTHONPATH"

/usr/local/bin/python3.5 ${NEUHOME}/neuralgae_bot.py -s Mastodon -c ${NEUHOME}/mastodon.yml
