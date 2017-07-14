#!/usr/bin/env python3.5

import re, requests, html
from botclient import Bot
import voronidols

class Voronidols(Bot):

    def voronoi(self):
        
        
if __name__ == '__main__':
    bot = Voronidols()
    bot.configure()
    vorofile = bot.voronoi()
    if vorofile:
        bot.wait()
        bot.post_image("", vorofile)
    else:
        print("Something went wrong")

