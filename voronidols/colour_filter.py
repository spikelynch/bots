#!/usr/bin/env python

import colorsys, sys

HUES = [ 0, 0.333 ]

TOLERANCE = 0.02

def to_hsv(parts):
    r = float(parts[0]) / 255.0
    g = float(parts[1]) / 255.0
    b = float(parts[2]) / 255.0
    return colorsys.rgb_to_hsv(r, g, b)


for l in sys.stdin.readlines():
    if l[0] == '#':
        next
    parts = l[:-1].split()
    if len(parts) == 4:
        ( h, s, v ) = to_hsv(parts)
        if s > 0:
            for h0 in HUES:
                if abs(h0 - h) <= TOLERANCE:
                    print(l[:-1])
                    next
    
