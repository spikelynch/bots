#!/usr/bin/env python3

import random, sys, re
from twitterbot import TwitterBot

class XIIScripta(TwitterBot):

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

