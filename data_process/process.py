from glob import glob
import csv
import numpy as np
import json

from Tracks import Tracks


class Process:
    def __init__(self):
        self.RECENT_TRACKS = "./data/user_recent_tracks/"
        self.matrix = []
        self.tracks = Tracks()
        self.tracks.prepare_tracks()


    def init(self):
        tracks = []

        files = glob(self.RECENT_TRACKS + "*.txt")

        for file in files:
            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                headers = reader.next()

                for row in reader:
                    tracks.append(row)

                self.matrix.append(self.process_line(tracks))


    def process_line(self, tracks):
        line = []

        for track in tracks:
            print ''


if __name__ == '__main__':
    process = Process()
    process.init()
