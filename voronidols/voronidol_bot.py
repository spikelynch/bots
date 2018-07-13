#!/usr/bin/env python3.5

import random, os.path, uuid

from botclient import Bot
from voronidols import mkcolours, voronidol
from iconoci import iconoci

class Voronidols(Bot):

    def voronoi(self):
        colours = mkcolours(colourfile=self.cf['colours_file'])
        f = '{}.png'.format(uuid.uuid1().hex)
        outfile = os.path.join(self.cf['working'], f)
        s = random.choice(self.cf['symmetry'])
        p = random.choice(list(range(self.cf['points_min'], self.cf['points_max'])))
        c = random.choice(list(range(self.cf['colours_min'], self.cf['colours_max'])))
        fr = random.uniform(self.cf['frame_min'], self.cf['frame_max'])
        w = self.cf['width']
        h = self.cf['height']
        return voronidol(w, h, p, s, c, colours, outfile, frame=fr)

        
if __name__ == '__main__':
    bot = Voronidols()
    bot.configure()
    vorofile = bot.voronoi()
    # Mastodon doesn't allow empty text in a media post so generate
    # a little symmetrical iconoci emoji to go with the voronidol
    text = iconoci(random.randrange(3, 12))
    if vorofile:
        bot.wait()
        options = {}
        if 'content_warning' in bot.cf:
            options['spoiler_text'] = bot.cf['content_warning'].format(text)
        if "description" in bot.cf:
            options['description'] = bot.cf['description'].format(text)
        if options: 
            options["sensitive"] = True
        bot.post_image(vorofile, text, options)
    else:
        print("Something went wrong")

