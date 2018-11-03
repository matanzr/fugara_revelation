import json
import os

class Playlist:    
    def __init__(self):
        self.list = []
        self.current_track = 0

    def getTrack(self):
        print "playlist: get track: # ", self.list[self.current_track]
        return self.list[self.current_track]
    
    def nextTrack(self):
        self.current_track = (self.current_track + 1) % len(self.list)
        print "playlist: next track: # ", self.current_track
   
    def add(self, seq_name, id, length):
        self.list.append([seq_name, id, length])
        print "playlist: Added track ", seq_name
   
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