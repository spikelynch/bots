#!/usr/bin/env python3

import os.path, re

from textbot import TextBot

class PictureBot(TextBot):
    """
Filereader bot which parses a text file and uses one field as a link to
an image - used for the rebuilt version of neuralgae

The method get_next() returns the next line as a ( file, text ) tuple 

Default config variables:

textfile
lastfile
index_re
images
"""


    def configure(self):
        """
Prepend the 'images' directory to the two file configs
"""
        super(PictureBot, self).configure(mandatory_fields=[ 'textfile', 'lastfile', 'images', 'index_re'])
        self.cf['textfile'] = os.path.join(self.cf['images'], self.cf['textfile'])
        self.cf['lastfile'] = os.path.join(self.cf['images'], self.cf['lastfile'])
    
    def get_next(self):
        """
Read the cf.lastfile to find the last image posted and look for the next line
in cf.textfile which matches cf.index_re. The first group is the image file and the second is the text to post as the tweet or toot.

Args:
    None

Returns:
    ( image, text ): (str, str): the image file and text
    ( none, none ): if there were no more images

"""
        image = None
        text = None
        index_re = re.compile(self.cf['index_re'])
        while not image:
            line = super(PictureBot, self).get_next()
            print(line)
            if not line:
                return ( None, None )
            m = index_re.search(line)
            if m:
                image = os.path.join(self.cf['images'], m.group(1))
                text = m.group(2)
            else:
                print("no match: {}".format(line))
        return ( image, text )

            
            
if __name__ == '__main__':
    bot = PictureBot()
    bot.configure()
    image, tweet = bot.get_next()
    if tweet:
        bot.post_image(image, tweet)
    else:
        print("Error")



