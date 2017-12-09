#!/usr/bin/env python3.5

from picturebot import PictureBot


        
if __name__ == '__main__':
    bot = PictureBot()
    bot.configure()
    ( image, text ) = bot.get_next()
    if text:
        text = text.replace('/','\n')
        bot.post_image(image, text)
    else:
        print("Couldn't find line to post")

