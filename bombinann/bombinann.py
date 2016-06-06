#!/usr/bin/env python

from twitterbot import TwitterBot
import torchrnn

import re

class BombinaNN(TwitterBot):

    def greptw(self, str):
        dv = re.compile('<div>(.*)</div>')
        m = dv.search(str)
        if m:
            tw = m.group(1)
            tw = tw.replace('<br />', '')
            return tw
        else:
            return None 

    def bombinan(self):
        twhtmls = torchrnn.generate_lines(model=self.cf['model'], n=10)
        for t in twhtmls:
            tt = self.greptw(t)
            if tt:
                return tt
        return None
        
if __name__ == '__main__':
    b = BombinaNN()
    b.configure()
    tweet = b.bombinan()
    if tweet:
        b.post(tweet)
    else:
        print("Something went wrong")

