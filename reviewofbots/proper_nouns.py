#!/usr/bin/env python

import nltk
from nltk.corpus import wordnet as wn

ss = wn.all_synsets(pos=wn.NOUN)

for s in ss:
    ws = [ l.name() for l in s.lemmas() ]
    for n, t in nltk.pos_tag(ws):
        if t == 'NNP' and len(n) > 3:
            print(n.replace('_', ' '))
