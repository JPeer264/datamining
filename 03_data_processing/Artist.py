import csv


class Artist:
    def __init__(self):
        self.DATA = './data/'
        self.ARTISTS_FILE = self.DATA + 'artists.txt'
        self.ARTISTS_TAGS_FILE = self.DATA + 'artists_with_tags.txt'

        self.artist_ids = []
        self.artits_with_tags = {}


    def prepare_artists(self):
        artist_ids = []
        artist_names = []

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()
            count = 0

            for row in reader:
                artist_ids.append(count)
                artist_names.append(row[headers.index("name")])
                count = count + 1

        self.artist_ids = artist_ids
        self.artist_names = artist_names

        with open(self.ARTISTS_TAGS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                if len(row) == 1:
                    self.artits_with_tags[row[0]] = []
                    continue

                self.artits_with_tags[row[0]] = row[1:]


    def get_artist_tags(self, artist_ref):
        if not artist_ref in self.artits_with_tags:
            return []

        return self.artits_with_tags[artist_ref]


    def get_artist_name(self, artist_ref):
        return self.artist_names[artist_ref]


if __name__ == '__main__':
    artist = Artist()
    artist.prepare_artists()
