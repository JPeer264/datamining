from glob import glob
import numpy as np
import json

import helper
from TracksGen import TracksGen


class ArtistsGen:
    def __init__(self):
        self.artists_line = ""
        self.all_tracks = []
        self.artist_names = []
        self.artist_mbid = []

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "artists.txt"

        self.USER_ARTISTS_LOOP = 'user_top_artists'
        self.TOP_ARTISTS_LOOP = 'top_artists'

    def compute(self):
        tracksGen = TracksGen(True)

        self.all_tracks = tracksGen.prepare_tracks()
        self.artists_line = self.artist_array_to_line("init")
        all_artists = self.prepare_artists()

        for artist in all_artists:
            self.artists_line = self.artists_line + \
                self.artist_array_to_line(artist)

    @staticmethod
    def get_artist_format():
        return ["name", "mbid"]

    def artist_array_to_line(self, artist="init"):
        artist_format = self.get_artist_format()
        line = ""

        if artist == "":
            return ""

        for i, entry in enumerate(artist_format):
            temp_line = "\t"

            if i == 0:
                temp_line = ""

            name = ""

            if artist == "init":
                name = entry
            else:
                name = artist[entry]

            line = line + temp_line + name

        return line + "\n"

    def get_artist_array(self, artist):
        name = artist['name'].encode('utf8')
        mbid = artist['mbid'].encode('utf8')

        # playcount = artist['playcount'].encode('utf8')

        # make sure the artist name or mbid exists
        if ((mbid == '') and (name in self.artist_names)) or (mbid in self.artist_mbid):
            return ""

        self.artist_names.extend([name])

        if not mbid == '':
            self.artist_mbid.extend([mbid])
        else:
            self.artist_mbid.extend([name])

        return {
            'name': name,
            'mbid': mbid,
        }

    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.artists_line)
        to_write_file.close()

    def prepare_artists(self):
        # loop over users top artists
        all_artists_array = []
        dirs = np.array(
            glob(self.FETCHED_DATA + self.USER_ARTISTS_LOOP + "/*/"))

        for user_dir in dirs:
            files = glob(user_dir + "*.json")

            for file in files:
                file_payload = json.load(open(file))
                artists = file_payload['topartists']['artist']

                for artist in artists:
                    artist_array = self.get_artist_array(artist)

                    if artist_array == "":
                        continue

                    all_artists_array.extend([artist_array])

        # loop over top artists
        files = glob(self.FETCHED_DATA + self.TOP_ARTISTS_LOOP + "/*.json")

        for file in files:
            file_payload = json.load(open(file))
            artists = file_payload['artists']['artist']

            for artist in artists:
                artist_array = self.get_artist_array(artist)

                if artist_array == "":
                    continue

                all_artists_array.extend([artist_array])

        # loop over all tracks from user
        # missing artists could be in there as well
        if self.all_tracks != []:
            for track in self.all_tracks:
                artist_array = self.get_artist_array({
                    "name": track["artist"].decode('utf8'),
                    "mbid": track["artist_mbid"].decode('utf8'),
                })

                if artist_array == "":
                    continue

                all_artists_array.extend([artist_array])

        return all_artists_array


# artistGen = ArtistsGen()
# artistGen.compute()
# artistGen.save()
