"""
bot - a basic Bot class
"""

from twython import Twython
import yaml

CHAR_LIMIT = 140
CHAR_LIMIT_IMG = 130

class TwitterBot(object):
    """Object which reads a config file and posts to Twitter.

Subclass this to add extra config checking and its own methods."""

    def __init__(self, configfile):
        self.config = None
        with open(configfile) as cf:
            try:
                self.cf = yaml.load(cf)
            except yaml.YAMLError as exc:
                print("%s parse error: %s" % ( conffile, exc ))
                if hasattr(exc, 'problem_mark'):
                    mark = exc.problem_mark
                    print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
        if not self.cf:
            print("Config error")
            sys.exit(-1)
        if not self.check_config():
            sys.exit(-1)

    def check_config(self):
        print("You should provide a check_config method")
        return False

    def auth(self):
        self.twitter = Twython(self.cf['api_key'], self.cf['api_secret'], self.cf['oauth_token'], self.cf['oauth_token_secret'])
        if self.twitter:
            return True
        else:
            return False
    
    def post(self, tweet):
        if self.auth():
            if len(tweet) > CHAR_LIMIT:
                return False
            else:
                self.twitter.update_status(status=tweet)
                return True
        else:
            return False
    
    def post_image(self, imgfile, tweet):
    """Post an image and text to the twitter account.

Args:
    img (str): image file
    text (str): text part of tweet

Returns:
    status (bool): True if the post was successful
"""
        if self.auth():
            print("Posting %s" % img)
            if len(text) > CHAR_LIMIT_IMG:
                return False
            with open(img, 'rb') as ih:
                response = self.twitter.upload_media(media=ih)
                out = self.twitter.update_status(status=text, media_ids=response['media_id'])
                return True
        else:
            return False
        
