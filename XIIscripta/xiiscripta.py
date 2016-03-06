#!/usr/bin/env python3

import random, sys, re
from twitterbot import TwitterBot

class XIIScripta(TwitterBot):

    # three sets of word pairs, which may be:
    # Verb Noun (nominative)
    # Verb Verb (infinitive, 

    
    def generate(self):
        self.a = "VENARI"
        self.b = "LAVARI"
        self.c = "LVDERE"
        self.d = "RIDERE"
        self.e = "OCCEST"
        self.f = "VIVERE"
        self.s = '+'
        

    
if __name__ == '__main__':
    bot = XIIScripta()
    bot.configure()
    bot.generate()
    tweet = bot.render()
    bot.post(tweet)
    print(tweet)

