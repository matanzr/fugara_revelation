class Playlist:
    def __init__(self):
        self.list = []
        self.current_track = 0

    def getTrack(self):
        return self.list[self.current_track]
    
    def nextTrack(self):
        self.current_track = self.current_track + 1 % len(self.list)
   
    def add(self, seq_name, id, length):
        self.list.append([seq_name, id, length])
   
    def remove(self, index):
        self.list.pop(index)