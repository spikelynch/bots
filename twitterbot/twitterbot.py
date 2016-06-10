"""
bot - a basic Bot class
"""

from twython import Twython
import argparse, yaml, pystache

CHAR_LIMIT = 140
CHAR_LIMIT_IMG = 130
TWITTER_CF = [ 'api_key', 'api_secret', 'oauth_token', 'oauth_token_secret' ]


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
        """Create a TwitterBot

The base class __init__ creates an argpase.ArgumentParser and adds two
arguments to it: --config (mndatory, the config file name) and --dry-run
(optional flag to just create the tweet and print to stdout rather than
post it).

To add more arguments in your subclass, call super().__init__ at the
start of your class's __init__ method.

This method doesn't parse the args (this is so that the subclass can add
new ones) - that's done in the configure method.
"""
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument('-c', '--config', required=True, type=str, help="Config file")
        self.ap.add_argument('-d', '--dry-run', action='store_true', help="Don't post")


    def configure(self, mandatory_fields=None):
        """Parse command-line arguments and read the config file.

If there are any missing arguments or reading the config file fails for any
reason, this calls sys.exit().

The Twitter authentication fields are checked by default, you don't need
to pass them in.
        """
        self.args = self.ap.parse_args()
        self.cf = None
        with open(self.args.config) as cf:
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
        fields = TWITTER_CF
        if mandatory_fields:
            fields += mandatory_fields
        cf_missing = False
        for field in fields:
            if not field in self.cf:
                print("Missing mandatory field: %s" % key)
                cf_missing = True
        if cf_missing:
            sys.exit(-1)

    def render(self):
        """Render a moustache template with this object and return the result"""
        pyr = pystache.Renderer()
        return pyr.render(self)


    def auth(self):
        """Authenticates against Twitter and returns true if successful"""
        self.twitter = Twython(self.cf['api_key'], self.cf['api_secret'], self.cf['oauth_token'], self.cf['oauth_token_secret'])
        if self.twitter:
            return True
        else:
            return False
    
    def post(self, tweet):
        """Post a string as a new tweet."""
        if len(tweet) > CHAR_LIMIT:
            print("Tweet text is over %d chars" % CHAR_LIMIT)
            return False
        if self.args.dry_run:
            print("Dry run: not posting")
            print("Tweet: %s" % tweet)
            return True
        if self.auth():
            self.twitter.update_status(status=tweet)
            return True
        else:
            return False
    
    def post_image(self, imgfile, tweet):
        """Post a tweet with one attached image

Args:
    img (str): image file
    text (str): text part of tweet

Returns:
    status (bool): True if the post was successful
       """
        if len(tweet) > CHAR_LIMIT_IMG:
            print("Tweet text is over %d chars" % CHAR_LIMIT_IMG)
            return False
        if self.args.dry_run:
            print("Dry run: not posting")
            print("Imagefile: %s" % imgfile)
            print("Tweet: %s" % tweet)
            return True
        if self.auth():
            print("Posting %s" % img)
            with open(img, 'rb') as ih:
                response = self.twitter.upload_media(media=ih)
                print("Tweet: %s" % tweet)
                out = self.twitter.update_status(status=tweet, media_ids=response['media_id'])
                return True
        else:
            return False
        
    def wait(self):
        """Wait for a random interval

        If there's a config variable 'pause', this method picks a random
        number between 0 and pause, and sleeps for that number of seconds.
        This is a simple way to make bot timing be less metronomic: you
        can set a cron job and then have a bit of scatter"""
        
        if 'pause' in self.cf:
            pause = random.randrange(0, int(self.cf['pause']))
            print("Waiting for {}".format(pause))
            time.sleep(pause)
