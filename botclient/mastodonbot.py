"""
mastodonbot 
"""

from mastodon import Mastodon


class MastodonBot(object):
    """A Mastodon bot class.

"""
    def __init__(cf):
        self.char_limit = 500
        self.char_limit_img = 500
        self.auth_cf_fields = [ 'api_key', 'api_secret', 'oauth_token', 'oauth_token_secret' ]
        self.cf = cf
            
    def auth(self):
        """Authenticates against Twitter and returns true if successful"""
        self.mast = Mastodon(self.cf['client_id'], self.cf['client_secret'], self.cf['access_token'], api_base_url=self.cf['base_url'])
        if self.mast:
            return True
        else:
            return False
    
    def post(self, toot):
        """Post a string as a new toot."""
        if len(toot) > self.char_limit:
            print("Toot text is over %d chars" % self.char_limit)
            return False
        if self.auth():
            status = self.mast.toot(toot)
            return True
        else:
            return False
    
    def post_image(self, imgfile, mimetype):
        """Post a toot with one attached image

Args:
    img (str): image file
    text (str): text part of toot

Returns:
    status (bool): True if the post was successful
       """
        if self.auth():
            print("Posting %s" % img)
            with open(img, 'rb') as ih:
            self.mast.media_post(imgfile, mimetype)
            return True
        else:
            return False
        
