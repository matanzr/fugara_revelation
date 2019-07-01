import json
import os
import pycron
import time

class Scheduler:    
    def __init__(self):
        self.list = []
        self.stopTime = None
   
    def add(self, cron_time, action):
        self.list.append([cron_time, action])
        print "scheduler: Added ", cron_time, action
   
    def remove(self, index):
        self.list.pop(index)

    def load(self, file):
        if not os.path.exists(file):
            return

        with open(file) as f:
            self.list = json.load(f)

        print "Playlist loaded from ", file
        print "Playlist contains ", len(self.list), "sequences"
        
    def save(self, file):
        with open(file, 'w') as outfile:
            json.dump(self.list, outfile)
    
    def isActive(self):
        if self.stopTime is not None:
            if time.time() > self.stopTime:
                self.stopTime = None
                print("stop")
                return "stop"
            return False

        for l in self.list:
            if pycron.is_now(l[0]): 
                self.stopTime = time.time() + 60*l[1]
                print ("playing, will stop in ", l[1], "minutes")
                return "play"
        
        return False