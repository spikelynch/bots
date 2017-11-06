#!/usr/bin/env python3.5

from botclient import PictureBot

        
if __name__ == '__main__':
    bot = PictureBot()
    bot.configure()
    ( image, text ) = bot.get_next()
    bot.post_image(image, text)

