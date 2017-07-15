#!/usr/bin/env python3.5

import re, requests, html, os.path, uuid

from botclient import Bot
from voronidols import mkcolours, voronidol

class Voronidols(Bot):

    def voronoi(self):
        colors = mkcolours(file=self.cf['colours_file'])
        f = '{}.png'.format(uuid.uuid1().hex)
        p = os.path.join(self.cf['working'], f)
        s = random.choice(self.cf['symmetry'])
        p = random.choice(list(range(self.cf['points_min'], self.cf['points_max'])))
        c = random.choice(list(range(self.cf['colours_min'], self.cf['colours_max'])))
        w = self.cf['width']
        h = self.cf['height']
        return voronidols.voronidol(w, h, p, s, c, colours, f)

        
if __name__ == '__main__':
    bot = Voronidols()
    bot.configure()
    vorofile = bot.voronoi()
    if vorofile:
        bot.wait()
        bot.post_image("", vorofile)
    else:
        print("Something went wrong")

