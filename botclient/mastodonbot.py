"""
mastodonbot 
"""

from mastodon import Mastodon


class MastodonBot(object):
    """A Mastodon bot class.

"""
    def __init__(self):
        self.char_limit = 500
        self.char_limit_img = 500
        self.auth_cf_fields = [ 'client_id', 'client_secret', 'access_token', 'base_url' ]
            
    def auth(self, cf):
        """Authenticates against Mastodon and returns true if successful"""
        self.mast = Mastodon(cf['client_id'], cf['client_secret'], cf['access_token'], api_base_url=cf['base_url'])
        if self.mast:
            return True
        else:
            return False
    
    def post(self, toot):
        """Post a string as a new toot."""
        if len(toot) > self.char_limit:
            print("Toot text is over %d chars" % self.char_limit)
            return False
        status = self.mast.toot(toot)
        return True
    
    def post_image(self, imgfile, text):
        """Post a toot with one attached image

Args:
    img (str): image file
    text (str): text part of toot

Returns:
    status (bool): True if the post was successful
       """
        print("Posting %s" % imgfile)
        image = self.mast.media_post(imgfile)
        if image:
            if not text:
                text = '.'
            post = self.mast.status_post(text, media_ids = [ image ])
        
