#!/usr/bin/env python

from twitterbot import TwitterBot
import torchrnn
import datetime, time, random, os.path, re, math

MAX_LENGTH = 140

START_TRIM = 100

class Usylessly(TwitterBot):

    def raw(self, temperature=1, start=''):
        raw = torchrnn.run_sample(
            self.cf['model'],
            temperature,
            start,
            self.cf['nchars'] + START_TRIM
            )
        return raw[START_TRIM:]
    
    def sentences(self, temperature=1, start=''):
        text = self.raw(temperature, self.cf['start_text'])
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError as e:
            return []
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^\b.+?\b\s+', '', text)
        ss = []
        for l in re.split('(?<=[.!?])\s+', text):
            ss.append(l)
        return ss

    def make_tweet(self, sentences):
        tw = None
        short = [ s for s in sentences if len(s) <= MAX_LENGTH ]
        if short:
            tw = random.choice(short)
        else:
            words = re.split('\s+', random.choice(sentences))
            molly = words.pop(0)
            while len(molly) < MAX_LENGTH:
                tw = molly
                molly += ' ' + words.pop(0)
        tw = re.sub(r'^\u2014', '\u2015', tw)
        return tw

    def time_to_temp(self):
        hour = datetime.datetime.now().hour
        s = 0.5 * (1 + math.cos(math.pi * hour / 12.0))
        h = self.cf['high']
        l = self.cf['low']
        return l + s * ( h - l )
    
if __name__ == '__main__':
    bot = Usylessly()
    bot.configure()
    temp = bot.time_to_temp()
    sents = bot.sentences(temperature=temp, start='')
    tweet = bot.make_tweet(sents)
    if tweet:
        print(tweet)
        bot.post(tweet)
    else:
        print("something went wrong")
