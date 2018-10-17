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