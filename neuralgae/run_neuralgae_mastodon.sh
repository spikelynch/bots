#!/bin/bash


NEUHOME="/Users/mike/Desktop/bots/neuralgae"
BCHOME="/Users/mike/Desktop/bots/botclient"

export PYTHONPATH="$BCHOME:$PYTHONPATH"

python ${NEUHOME}/neuralgae_bot.py -s Mastodon -c ${NEUHOME}/mastodon_config.yml
