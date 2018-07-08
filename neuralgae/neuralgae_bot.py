#!/usr/bin/env python3.5

from picturebot import PictureBot

def build_content_warning(cwtemplate, text):
    lines = text.split('\n')
    cw = cwtemplate.format(lines[0])
    return cw


        
if __name__ == '__main__':
    bot = PictureBot()
    bot.configure()
    ( image, text ) = bot.get_next()
    if text:
        text = text.replace('/','\n')
        if bot.cf["content_warning"]:
            cw = build_content_warning(bot.cf["content_warning"], text)
            bot.post_image(image, text, { "spoiler_text": cw, "sensitive": True })
        else:
            bot.post_image(image, text)
    else:
        print("Couldn't find line to post")

