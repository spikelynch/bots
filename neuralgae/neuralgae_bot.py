#!/usr/bin/env python3.5

from picturebot import PictureBot

if __name__ == '__main__':
    bot = PictureBot()
    bot.configure()
    ( image, text ) = bot.get_next()
    if text:
        firstline = text.split('/')[0]
        text = text.replace('/','\n')
        options = {}
        if "content_warning" in bot.cf:
            options['spoiler_text'] = bot.cf['content_warning'].format(firstline)
        if "description" in bot.cf:
            options['description'] = bot.cf['description'].format(firstline)
        if options: 
            options["sensitive"] = True
            bot.post_image(image, text, options)
        else:
            bot.post_image(image, text)
    else:
        print("Couldn't find line to post")

