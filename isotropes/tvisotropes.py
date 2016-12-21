#!/usr/bin/env python3

import json, random, string, requests, re, html
import nltk
from nltk.tokenize import word_tokenize
from twitterbot import TwitterBot

elements = None

UNCONTRACT = {
    r"(\w) 're": r"\1're",
    r"(\w) 've": r"\1've",
    r"(\w) 'll": r"\1've",
    r"(\w) n't": r"\1n't",
    r"(\w) 's":  r"\1's",
    r"([cC])an not": r"\1annot",
    r"([Dd]) 'ye": r"\1'ye",
    r"([gG])im me": r"\1imme",
    r"([gG])on na": r"\1onna",
    r"([gG])ot ta": r"\1otta",
    r"([lL])em me": r"\1emme",
    r"'([Tt]) is": r"'\1is",
    r"'([Tt]) was": r"'\1was",
    r"([Ww])an na": r"\1anna"
}


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


    def uncontract(self, words):
        uw = []
        skipnext = False
        for i in range(0, len(words) - 1):
            if skipnext:
                skipnext = False
                continue
            w1 = words[i]
            w2 = words[i + 1]
            for p, s in UNCONTRACT.items():
                r = re.sub(p, s, w1 + " " + w2)
                if r != w1 + " " + w2:
                    uw.append(r)
                    skipnext = True
                    break
            if not skipnext:
                uw.append(w1)
        uw.append(words[-1])
        return uw
    

    def get_isotrope(self):
        title = None
        if 'test_title' in self.cf:
            title = self.cf['test_title']
        else:
            title = self.url_title()
        if title:
            words = word_tokenize(title)
            words = self.uncontract(words)
            if len(words) > 1:
                tagged = nltk.pos_tag(words)
                i = 0
                cnouns = []
                pos_re = re.compile(self.cf['pos_tags'])
                for ( w, pos ) in tagged:
                    mm = pos_re.search(pos)
                    if mm:
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
        return re.sub(r"\s([.,:;!?])", r"\1", q4)
    

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
