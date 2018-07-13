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
    
    def post(self, toot, options=None):
        """Post a string as a new toot."""
        if len(toot) > self.char_limit:
            print("Toot text is over %d chars" % self.char_limit)
            return False
        if options:
            status = self.mast.status_post(toot, **options)
        else:
            status = self.mast.status_post(toot)
        return True
    
    def post_image(self, imgfile, text, options=None):
        """Post a toot with one attached image

Args:
    img (str): image file
    text (str): text part of toot
    options (dict): options, see the Mastodon.py docs

Returns:
    status (bool): True if the post was successful
       """
        print("Posting %s" % imgfile)
        if 'description' in options:
            image = self.mast.media_post(imgfile, mime_type=None, description=options['description'])
            del options['description']
        else:
            image = self.mast.media_post(imgfile)
        if image:
            if not text:
                text = '.'
            if options:
                post = self.mast.status_post(text, media_ids=[ image ], **options)
            else:
                post = self.mast.status_post(text, media_ids=[ image ])

