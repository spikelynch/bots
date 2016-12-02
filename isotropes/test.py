#!/usr/bin/env python3

import json, random, string, requests, re
import nltk
from nltk.tokenize import word_tokenize

ELEMENTS = 'elements.json'
TROPE_URL = 'http://tvtropes.org/pmwiki/randomitem.php?p=1'
TROPE_RE = '<title>(.*) - TV Tropes'
elements = None

with open(ELEMENTS) as ef:
    ej = json.load(ef)
    if ej:
        elements = ej['elements']

def get_elements(es, start):
    with_start = [ e['name'] for e in es if e['name'][0] == start ]
    if with_start:
        return random.choice(with_start)
    else:
        return(None)

def get_isotrope(es):
    title_re = re.compile(TROPE_RE)
    r = requests.get(TROPE_URL)
    if r.status_code == 200:
        m = title_re.search(r.text)
        if m:
            title = m.group(1)
            words = word_tokenize(title)
            if len(words) > 1:
                tagged = nltk.pos_tag(words)
                i = 0
                cnouns = []
                for ( w, pos ) in tagged:
                    if pos[:2] == 'NN':
                        e = get_elements(elements, w[0])
                        if e:
                            cnouns.append((i, e))
                    i += 1
                if cnouns:
                    return ( tagged, cnouns )
    return ( None, None )

# for l in string.ascii_uppercase:
#     with_start = [ e['name'] for e in elements if e['name'][0] == l ]
#     print(l, with_start)


for i in range(0, 20):
    tagged = None

    while not tagged:
        ( tagged, cnouns ) = get_isotrope(elements)

    (ci, n) = random.choice(cnouns)
    words = [ t[0] for t in tagged ]
    words[ci] = n
    print(' '.join(words))

        
