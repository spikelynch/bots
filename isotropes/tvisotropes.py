#!/usr/bin/env python3

import json, random, string, requests, re, html
import nltk
from nltk.tokenize import word_tokenize
from twitterbot import TwitterBot

elements = None


# for l in string.ascii_uppercase:
#     with_start = [ e['name'] for e in elements if e['name'][0] == l ]
#     print(l, with_start)




class TVisoTropes(TwitterBot):

    def read_elements(self):
        ej = None
        with open(self.cf['elements']) as ef:
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

    def url_title(self):
        title_re = re.compile(self.cf['trope_re'])
        url = self.cf['trope_url']
        if 'trope_test_url' in self.cf:
            url = self.cf['trope_test_url']
        r = requests.get(url)
        if r.status_code == 200:
            m = title_re.search(r.text)
            if m:
                title = m.group(1)
                title = html.unescape(title)
                return title
        return None

    def get_isotrope(self):
        title = None
        if 'test_title' in self.cf:
            title = self.cf['test_title']
        else:
            title = self.url_title()
        if title:
            print("unesc title " + title)
            words = word_tokenize(title)
            print("tokenised " + ', '.join(words))
            if len(words) > 1:
                tagged = nltk.pos_tag(words)
                i = 0
                cnouns = []
                print(self.cf['pos_tags'])
                pos_re = re.compile(self.cf['pos_tags'])
                for ( w, pos ) in tagged:
                    mm = pos_re.search(pos)
                    if mm:
                        print("Matched " + w + " '" + pos + "'")
                        print(mm.group(0), mm.group(1))
                        e = self.get_element(w[0])
                        if e:
                            cnouns.append((i, e))
                    i += 1
                if cnouns:
                    return ( tagged, cnouns )
        return ( None, None )

    def smart_join(self, words):
        basic = ' '.join(words)
        # nltk tokenizer turns "foo" into ``foo'' - turn it back
        q1 = re.sub(r" `` ", r' "', basic)
        q2 = re.sub(r"`` ", r'"', q1)
        q3 = re.sub(r" '' ", r'" ', q2)
        q4 = re.sub(r" ''", r'"', q3)
        q5 = re.sub(r" n't ", r"n't ", q4)
        q6 = re.sub(r" '([a-z]) ", r"'\1 ", q5)
        q7 = re.sub(r"\b '", r"'", q6)
        return re.sub(r"\s([.,:;!?])", r"\1", q7)
    

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
