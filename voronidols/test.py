#!/usr/bin/env python3.5

import voronidols, random

SYMM = [ 'vertical' ] #, 'horizontal', 'both', 'rot2', 'rot4' ]


def random_voro(f):
    s = random.choice(SYMM)
    p = random.choice(list(range(4, 80)))
    c = random.choice(list(range(5, 10)))
    k = random.uniform(.2, 1)
    colours = voronidols.mkcolours()
    return voronidols.voronidol(640, 480, p, s, c, colours, f)




for i in range(5):
    f = 'voro{}.png'.format(i)
    random_voro(f)

