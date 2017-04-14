#!/usr/bin/env python3.5

import re, requests, html
from botclient import Bot

WIKI_RANDOM_URL = 'https://en.wikipedia.org/wiki/Special:Random'
WIKI_TITLE_RE = '<title>(.*) -'

TWEET_TEMPLATE = 'Talking {} Blues'

class TalkingBotBlues(Bot):

    def got_the_blues(self):
        title_re = re.compile(self.cf['title_re'])
        r = requests.get(self.cf['wiki_url'])
        if r.status_code == 200:
            m = title_re.search(r.text)
            if m:
                title = m.group(1)
                title = html.unescape(title)
                words = [ self.capmaybe(w) for w in title.split(' ') ]
                title = ' '.join(words)
                return self.cf['tweet_template'].format(title)
        return None

    def capmaybe(self, word):
        if word in self.cf['nocaps']:
            return word
        else:
            if word[0] == '(':
                return word[0] + word[1].upper() + word[2:]
            else:
                return word[0].upper() + word[1:]
        
        
if __name__ == '__main__':
    bot = TalkingBotBlues()
    bot.configure()
    tweet = bot.got_the_blues()
    if tweet:
        bot.wait()
        bot.post(tweet)
    else:
        print("Something went wrong")

