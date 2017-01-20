#!/usr/bin/env python3.5

import random, sys
from twitterbot import TwitterBot



class ReviewOfBots(TwitterBot):

    def __init__(self):
        super().__init__()
        self.ap.add_argument('-n', '--number', type=int, default=None, help="Run n times without posting")
        
    def loadfile(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            return [ l.strip() for l in lines ]
        
    def load(self):
        self.lists = []
        for fn in self.cf['wordlists']:
            self.lists.append(self.loadfile(fn))
        
    def render(self):
        w = random.choice(random.choice(self.lists))
        t = w.title()
        t = t.replace("'S", "’s")
        return self.cf['tweet_template'].format(t)

        
if __name__ == '__main__':
    rob = ReviewOfBots()
    rob.configure()
    rob.load()
    if rob.args.number:
        for i in range(rob.args.number):
            print(rob.render())
    else:
        tweet = rob.render()
        rob.wait()
        rob.post(tweet)
        print(tweet)

