#!/usr/bin/env python3.5

from nltk.corpus import wordnet as wn
import random, sys, re
from twitterbot import TwitterBot

# Synsets which are offensive but not flagged as such in the
# WordNet definition
SLUR_SS = [ 'native.n.01', 'aborigine.n.02' ] 


def random_word(synsets):
    synset = random.choice(synsets)
    lemma = random.choice(synset.lemmas())
    name = lemma.name()
    return name.replace('_', ' ')

def is_not_slur(synset):
    if synset.name() in SLUR_SS:
        return False
    d = synset.definition()
    if 'slur' in d or 'offensive' in d:
        return False
    else:
        return True

class Quest(TwitterBot):
    def __init__(self):
        super().__init__()
        self.ap.add_argument('-t', '--test', action='store_true', help="Don't post, dump list of all nouns to test for bad words")
        self.ap.add_argument('-n', '--noun', type=str, help="synset id to force a noun")

    def read_words(self):
        self.nouns = [ s for s in wn.all_synsets(pos=wn.NOUN) if is_not_slur(s) ]
        self.verbs = list(wn.all_synsets(pos=wn.VERB))

    def randomise(self):
        self.read_words()
        synset = self.args.noun
        if synset:
            ss = wn.synset(synset)
            if ss:
                self.noun = random_word([ss]).upper()
                print("Noun = %s" % self.noun)
            else:
                print("Couldn't find synset %s" % synset)
                sys.exit(-1)
        else:
            self.noun = random_word(self.nouns).upper()
        self.verb = random_word(self.verbs).upper()

    def dump_nouns(self):
        self.read_words()
        for s in self.nouns:
            print(s.name(), s.definition())
            for l in s.lemmas():
                print(l.name())

        
if __name__ == '__main__':
    q = Quest()
    q.configure()
    if q.args.test:
        q.dump_nouns()
        sys.exit(1)
    q.randomise()
    tweet = q.render()
    q.post(tweet)
    print(tweet)

