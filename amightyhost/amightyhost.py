#!/usr/bin/env python

from twitterbot import TwitterBot
import subprocess

class AMightyHost(TwitterBot):

    def warriors(self):
        cmd = [ self.cf['exe'], self.cf['data'] ]
        army = subprocess.check_output(cmd)
        return army[:-1]
        
if __name__ == '__main__':
    amh = AMightyHost()
    amh.configure()
    tweet = amh.warriors()
    if tweet:
        amh.wait()
        amh.post(tweet)
    else:
        print("Something went wrong")

