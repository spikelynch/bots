#!/usr/bin/env python

from botclient import Bot
import torchrnn
import sys, datetime, time, random, os.path, re, math

MAX_LENGTH = 140
MAX_REPEATS = 10

START_TRIM = 100

class Usylessly(Bot):
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
        temp = None
        if self.args.episode:
            if self.args.episode in self.cf['episodes']:
                seeds = self.cf['episodes'][self.args.episode]['seeds']
                seed = random.choice(seeds.split(' '))
                print("Seed: {}".format(seed))
                temp = float(self.cf['episodes'][self.args.episode]['temp'])
                print("Temp: {}".format(temp))
        if not temp:
            temp = self.time_to_temp(hour=hour)
        text = self.raw(temp, seed)
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
        chunks = [ s for s in sentences[1:] if len(s) <= MAX_LENGTH ]
        if not len(chunks):
            chunks = re.split('\s+', random.choice(sentences))
        para = chunks.pop(0)
        while len(para) < MAX_LENGTH:
            tw = para
            para += ' ' + chunks.pop(0)
        if tw:
            tw = re.sub(r' \u2014', '\n\u2015', tw)
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

    def ulyssitise(self):
        reps = 0
        tw = None
        while not tw and reps < MAX_REPEATS:
            sents = self.sentences()
            tw = self.make_tweet(sents)
            reps += 1
        return tw
    
    
if __name__ == '__main__':
    bot = Usylessly()
    bot.configure()
    tweet = bot.ulyssitise()
    if tweet:
        print(tweet)
        options = {}
        if 'content_warning' in bot.cf:
            options['spoiler_text'] = bot.cf['content_warning']
        bot.post(tweet, options)
    else:
        print("something went wrong")
