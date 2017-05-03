#!/usr/bin/env python

from botclient import Bot
import subprocess

class Kerlossal(Bot):

    def artwork(self):
        cmd = [ self.cf['exe'], self.cf['data'] ]
        if 'max_length' in self.cf:
            cmd.append(self.cf['max_length'])
        result = subprocess.check_output(cmd)
        return result[:-1]
        
if __name__ == '__main__':
    k = Kerlossal()
    k.configure()
    tweet = k.artwork()
    if tweet:
        k.wait()
        k.post(tweet)
    else:
        print("Something went wrong")

