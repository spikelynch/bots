#!/usr/bin/env python

from botclient import Bot
import subprocess

class AMightyHost(Bot):

    def warriors(self):
        cmd = [ self.cf['exe'], self.cf['data'] ]
        army = subprocess.check_output(cmd)
        return army[:-1]
        
if __name__ == '__main__':
    amh = AMightyHost()
    amh.configure()
    band = amh.warriors()
    if band:
        amh.wait()
        amh.post(band)
    else:
        print("Something went wrong")

