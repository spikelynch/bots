#!/usr/bin/env python3

from nltk.corpus import wordnet as wn
import sys, argparse, inflect


def explode_hyponyms(ss):
    hs = ss.hyponyms()
    l = []
    if hs:
        for h in hs:
            l += explode_hyponyms(h)
        return l
    else:
        return [ ss ]


def wordlist(synsets, plurals=False):
    names = []
    pl = inflect.engine()

    for s in synsets:
        name = s.lemmas()[0].name()
        if plurals:
            name = pl.plural(name)
        name = name.replace('_', ' ')
        names.append(name)
    names = list(set(names))
    return names

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--synset", type=str, default="animal", help="Synset to dump hyponyms of")
parser.add_argument("-p", "--plurals", action='store_true', help="Generate plurals", default=False)


args = parser.parse_args()
    
synsets = wn.synsets(args.synset)
if not synsets:
    print("Couldn't find synset");
    sys.exit(-1)

sets = []
    
for ss in synsets:
    sets += explode_hyponyms(ss)
    
words = wordlist(sets, args.plurals)



for word in words:
    print(word)
