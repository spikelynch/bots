#!/usr/bin/env python3

import json, random, string, requests, re
import nltk
from nltk.tokenize import word_tokenize
from twitterbot import TwitterBot

ELEMENTS = 'elements.json'
TROPE_URL = 'http://tvtropes.org/pmwiki/randomitem.php?p=1'
TROPE_RE = '<title>(.*) - TV Tropes'
elements = None


# for l in string.ascii_uppercase:
#     with_start = [ e['name'] for e in elements if e['name'][0] == l ]
#     print(l, with_start)




class TVisoTropes(TwitterBot):

    def read_elements(self):
        ej = None
        with open(ELEMENTS) as ef:
            ej = json.load(ef)
        if ej:
            self.elements = ej['elements']
        else:
            sys.exit(-1)

    def get_element(self, start):
        with_start = [ e['name'] for e in self.elements if e['name'][0] == start ]
        if with_start:
            return random.choice(with_start)
        else:
            return(None)

    def get_isotrope(self):
        title_re = re.compile(self.cf['trope_re'])
        r = requests.get(self.cf['trope_url'])
        if r.status_code == 200:
            m = title_re.search(r.text)
            if m:
                title = m.group(1)
                words = word_tokenize(title)
                if len(words) > 1:
                    tagged = nltk.pos_tag(words)
                    i = 0
                    cnouns = []
                    for ( w, pos ) in tagged:
                        if pos[:2] == 'NN':
                            e = self.get_element(w[0])
                            if e:
                                cnouns.append((i, e))
                        i += 1
                    if cnouns:
                        return ( tagged, cnouns )
        return ( None, None )

    def smart_join(self, words):
        basic = ' '.join(words)
        return re.sub(r"\s([.,:;!?])", r"\1", basic)
    

    def render(self):
        tagged = None
        cnouns = None
        i = self.cf['max_repeats']
        while (not tagged) and i > 0:
            ( tagged, cnouns ) = self.get_isotrope()
            i -= 1
        if tagged:
            (ci, n) = random.choice(cnouns)
            words = [ t[0] for t in tagged ]
            words[ci] = n
            itext = self.smart_join(words)
            return itext
        return None
    
        
if __name__ == '__main__':
    b = TVisoTropes()
    b.configure()
    b.read_elements()
    
    tweet = b.render()
    if tweet:
        b.wait()
        b.post(tweet)
        print(tweet)
    else:
        print("No luck")
