#!/usr/bin/env python3

import random

SYMM = '!^*-_=+WwTYUIOo|AH:"\'XxM.'
PAIRS = [ '/\\', r'{}', r'[]', r'()', r'<>' ]

def rnd_pair():
    n = len(SYMM) + len(PAIRS)
    i = random.choice(list(range(n)))
    if i < len(SYMM):
        return SYMM[i], SYMM[i]
    else:
        i = i - len(SYMM)
        if random.choice([0, 1]):
            return PAIRS[i][0], PAIRS[i][1]
        else:
            return PAIRS[i][1], PAIRS[i][0]

def rnd_centre():
    return random.choice(SYMM)
    

def iconoci(l):
    if l % 2:
        s = rnd_centre()
    else:
        s = ''
    while len(s) < l:
        a, b = rnd_pair()
        s = a + s + b
    return s

