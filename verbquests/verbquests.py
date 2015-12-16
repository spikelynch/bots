#!/usr/bin/env python3.5

from nltk.corpus import wordnet as wn
from twython import Twython
import random, pystache, yaml, sys, argparse
import re

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

class Quest(object):
    def __init__(self, synset):
        self.nouns = [ s for s in wn.all_synsets(pos=wn.NOUN) if is_not_slur(s) ]
        self.verbs = list(wn.all_synsets(pos=wn.VERB))
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

def load_config(conffile):
    """Reads the YAML config file and returns a dict"""
    config = None
    with open(conffile) as cf:
        try:
            config = yaml.load(cf)
        except yaml.YAMLError as exc:
            print("%s parse error: %s" % ( conffile, exc ))
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
    if not config:
        print("Config error")
        sys.exit(-1)
    return config


def dump_nouns(q):
    for s in q.nouns:
        if "'" in s.name():
            print(s.name(), s.definition())
            for l in s.lemmas():
                print(l.name())

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, type=str, help="Config file")
    parser.add_argument('-d', '--dry-run', action='store_true', help="Don't post")
    parser.add_argument('-t', '--test', action='store_true', help="Don't post, dump list of all nouns to test for bad words")
    parser.add_argument('-n', '--noun', type=str, help="synset id to force a noun")
    args = parser.parse_args()
    cf = load_config(args.config)
    q = Quest(args.noun)
    if args.test:
        dump_nouns(q)
        sys.exit(1)
    pyr = pystache.Renderer()
    tweet = pyr.render(q)
    print(tweet)
    if args.dry_run:
        print("(dry run)")
    else:
        twitter = Twython(cf['api_key'], cf['api_secret'], cf['oauth_token'], cf['oauth_token_secret'])
        out = twitter.update_status(status=tweet)
        print("Posted")

