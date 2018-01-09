import csv

from Artist import Artist

class Tracks:
    def __init__(self):
        self.DATA = './data/'
        self.TRACKS_FILE = self.DATA + 'tracks.txt'

        self.track_ids = []
        self.artist_ids = []
        self.artists = Artist()
        self.artists.prepare_artists()

    def prepare_tracks(self):
        track_ids = []
        artist_ids = []

        with open(self.TRACKS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()[0].split(' ')
            count = 0

            for row in reader:
                track_ids.append(count)
                artist_ids.append(row[headers.index("artist_ref")])
                count = count + 1

        self.track_ids = track_ids
        self.artist_ids = artist_ids

    def get_tags(self, track_ref):
        try:
            artist_ref = self.artist_ids[int(track_ref)]
        except IndexError:
            return []
        except ValueError:
            return []

        return self.artists.get_artist_tags(artist_ref)


if __name__ == '__main__':
    tracks = Tracks()
    tracks.prepare_tracks()
