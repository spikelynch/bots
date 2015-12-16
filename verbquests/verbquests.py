#!/usr/bin/env python3

from nltk.corpus import wordnet as wn
from twython import Twython
import random, pystache, yaml, sys, argparse



def random_word(synsets):
    synset = random.choice(synsets)
    lemma = random.choice(synset.lemmas())
    name = lemma.name()
    return name.replace('_', ' ')

def is_not_slur(synset):
    d = synset.definition()
    if 'slur' in d or 'offensive' in d:
        return False
    else:
        return True

class Quest(object):
    def __init__(self):
        self.nouns = [ s for s in wn.all_synsets(pos=wn.NOUN) if is_not_slur(s) ]
        self.verbs = list(wn.all_synsets(pos=wn.VERB))
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

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, type=str, help="Config file")
    parser.add_argument('-d', '--dry-run', action='store_true', help="Don't post")
    args = parser.parse_args()
    cf = load_config(args.config)
    q = Quest()
    pyr = pystache.Renderer()
    tweet = pyr.render(q)
    print(tweet)
    if args.dry_run:
        print("(dry run)")
    else:
        twitter = Twython(cf['api_key'], cf['api_secret'], cf['oauth_token'], cf['oauth_token_secret'])
        out = twitter.update_status(status=tweet)
        print("Posted")

