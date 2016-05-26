#!/usr/bin/env python

from twitterbot import TwitterBot
import subprocess

class AMightyHost(TwitterBot):

    def warriots(self):
        cmd = [ self.cf['exe'], self.cf['data'] ]
        army = subprocss.check_output(cmd)
        
if __name__ == '__main__':
    amh = AMightyHost()
    amh.configure()
    tweet = amh.warriors()
    if tweet:
        amh.post(tweet)
    else:
        print("Something went wrong")

