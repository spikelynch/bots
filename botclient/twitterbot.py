"""
bot - a basic Bot class
"""

from twython import Twython


class TwitterBot(object):
    """A Twitter bot base class.

This is a base class for Twitter bots which provides methods to do the
authentication and posting (of text-only tweets and ones with images),
plus a few commonly-needed functions like parsing command-line arguments,
reading a config file and filling out templates.

Attributes:
    ap (ArgumentParser): the argument parser
    args (Namespace): the results of the argument parse
    cf (dict): the values read from the config file
    twitter (Twython): the Twython object used for the actual post
"""

    def __init__(self):
        self.char_limit = 140
        self.char_limit_img = 130
        self.auth_cf_fields = [ 'api_key', 'api_secret', 'oauth_token', 'oauth_token_secret' ]
    
    def auth(self, cf):
        """Authenticates against Twitter and returns true if successful"""
        self.twitter = Twython(cf['api_key'], cf['api_secret'], cf['oauth_token'], cf['oauth_token_secret'])
        if self.twitter:
            return True
        else:
            return False
    
    def post(self, tweet):
        """Post a string as a new tweet."""
        if len(tweet) > self.char_limit:
            print("Tweet text is over %d chars" % self.char_limit)
            return False
        self.twitter.update_status(status=tweet)
        return True
    
    def post_image(self, imgfile, tweet):
        """Post a tweet with one attached image

Args:
    img (str): image file
    text (str): text part of tweet

Returns:
    status (bool): True if the post was successful
       """
        if len(tweet) > self.char_limit_img:
            print("Tweet text is over %d chars" % self.char_limit_img)
            return False
        print("Posting %s" % imgfile)
        with open(imgfile, 'rb') as ih:
            response = self.twitter.upload_media(media=ih)
            print("Tweet: %s" % tweet)
            out = self.twitter.update_status(status=tweet, media_ids=response['media_id'])
            return True
        
