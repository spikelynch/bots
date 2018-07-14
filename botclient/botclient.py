"""
bot - a basic Bot class
"""

from twitterbot import TwitterBot
from mastodonbot import MastodonBot

import argparse, yaml, pystache, random, time, sys

SERVICES = {
    'Twitter': TwitterBot,
    'Mastodon': MastodonBot
    }


class Bot(object):
    """A bot base class.

This is a base class for bots which provides methods to do the
authentication and posting (of text-only tweets and ones with images),
plus a few commonly-needed functions like parsing command-line arguments,
reading a config file and filling out templates.

Attributes:
    ap (ArgumentParser): the argument parser
    args (Namespace): the results of the argument parse
    cf (dict): the values read from the config file
"""

    def __init__(self):
        """Create a Bot

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
        self.ap.add_argument('-s', '--service', default="Twitter", help="Twitter or Mastodon")
        self.ap.add_argument('-c', '--config', required=True, type=str, help="Config file")
        self.ap.add_argument('-d', '--dry-run', action='store_true', help="Don't post")


    def configure(self, mandatory_fields=None):
        """Parse command-line arguments and read the config file.

If there are any missing arguments or reading the config file fails for any
reason, this calls sys.exit().

        """
        self.args = self.ap.parse_args()
        if self.args.service not in SERVICES:
            print("Don't know how to post to {}".format(self.args.service))
            sys.exit(-1)
        self.api = SERVICES[self.args.service]()
        self.cf = None
        with open(self.args.config) as cf:
            try:
                self.cf = yaml.load(cf)
            except yaml.YAMLError as exc:
                print("%s parse error: %s" % ( self.args.config, exc ))
                if hasattr(exc, 'problem_mark'):
                    mark = exc.problem_mark
                    print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
        if not self.cf:
            print("Config error")
            sys.exit(-1)
        fields = self.api.auth_cf_fields
        if mandatory_fields:
            fields += mandatory_fields
        cf_missing = False
        for field in fields:
            if not field in self.cf:
                print("Missing mandatory field: %s" % field)
                cf_missing = True
        if cf_missing:
            sys.exit(-1)

    def render(self):
        """Render a moustache template with this object and return the result"""
        pyr = pystache.Renderer()
        return pyr.render(self)


    def post(self, text, options=None):
        """Post a string, or write it to stdout if we're dry-run"""
        if self.args.dry_run:
            print("Dry run: not posting")
            print("Status: %s" % text)
            if options:
                print("Options: %s" % options)
            return True
        if self.api.auth(self.cf):
            return self.api.post(text, options)
    
    def post_image(self, imgfile, text, options=None):
        """Post a tweet with one attached image

Args:
    img (str): image file
    text (str): text part of post

Returns:
    status (bool): True if the post was successful
       """
        if self.args.dry_run:
            print("Dry run: not posting")
            print("Imagefile: %s" % imgfile)
            print("Text: %s" % text)
            if options:
                print("Options: %s" % options)
            return True
        if self.api.auth(self.cf):
            return self.api.post_image(imgfile, text, options)
        
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
