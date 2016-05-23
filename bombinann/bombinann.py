#!/usr/bin/env python

from twitterbot import TwitterBot
import torchrnn

import re

class BombinaNN(TwitterBot):

    def bombianann(self):
        twhtmls = torchrnn.generate_lines(model=self.cf['model'])
        if twhtmls:
            dv = re.compile('<div>.*</div>')
            m = dv.search(twhtmls[0])
            if m:
                tw = m.groups(1)
                tw = tw.replace('<br />', '')
                return tw
        
        
if __name__ == '__main__':
    b = BombinaNNM()
    b.configure()
    tweet = b.bombinann()
    if tweet:
        bot.post(tweet)
    else:
        print("Something went wrong")

