#!/usr/bin/env python

from twitterbot import TwitterBot
import torchrnn
import sys, datetime, time, random, os.path, re, math

MAX_LENGTH = 140

START_TRIM = 100

class Usylessly(TwitterBot):
    def __init__(self):
        super().__init__()
        self.ap.add_argument('-e', '--episode', type=str, default=None, help="Config file")

        
    def raw(self, temperature=1, start=''):
        raw = torchrnn.run_sample(
            self.cf['model'],
            temperature,
            start,
            self.cf['nchars'] + START_TRIM
            )
        return raw[START_TRIM:]
    
    def sentences(self):
        seed = ""
        hour = None
        if self.args.episode:
            if self.args.episode in self.cf['episodes']:
                seeds = self.cf['episodes'][self.args.episode]['seeds']
                seed = random.choice(seeds.split(' '))
                print("Seed: {}".format(seed))
                hour = int(self.cf['episodes'][self.args.episode]['hour'])
        temperature = self.time_to_temp(hour=hour)
        text = self.raw(temperature, seed)
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

    def time_to_temp(self, hour=None):
        if not hour:
            hour = datetime.datetime.now().hour
        print("Hour {}".format(hour))
        s = 0.5 * (1 + math.cos(math.pi * hour / 12.0))
        h = self.cf['high']
        l = self.cf['low']
        t = l + s * ( h - l )
        print("Temperature {}".format(t))
        return t
    
if __name__ == '__main__':
    bot = Usylessly()
    bot.configure()
    sents = bot.sentences()
    tweet = bot.make_tweet(sents)
    if tweet:
        print(tweet)
        bot.post(tweet)
    else:
        print("something went wrong")
