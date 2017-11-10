#!/usr/bin/env python3

import os.path

from botclient import Bot

class TextBot(Bot):
    """
Generic filereader bot.

Tweets a line at a time from a text file, and saves the last line sent in
a state file to remember where it's up to.

Just run 'textbot.py' with the standard config files, or to give it extra
functionality, import TextBot and subclass it.

The method get_next() returns the next line.


Default config variables:

textfile
lastfile
"""
    
    def get_next(self):
        last = self.read_last()
        nextline = None
        with open(self.cf['textfile']) as bf:
            if not last:
                nextline = next(bf)
            else:
                for line in bf:
                    if line == last:
                        nextline = next(bf)
            print(nextline)
        if nextline:
            self.write_last(nextline)
        return nextline

    def read_last(self):
        if os.path.exists(self.cf['lastfile']):
            with open(self.cf['lastfile']) as lf:
                last = next(lf)
                return last
        return None

    def write_last(self, lastline):
        with open(self.cf['lastfile'], 'w') as lf:
            lf.write(lastline)
        
            
if __name__ == '__main__':
    bot = TextBot()
    bot.configure()
    tweet = bot.get_next()
    if tweet:
        bot.post(tweet)
    else:
        print("Error")

