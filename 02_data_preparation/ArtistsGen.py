from glob import glob
import numpy as np
import re

try:
    import ujson as json
except ImportError:
    import json

import helper
from TracksGen import TracksGen


class ArtistsGen:
    def __init__(self):
        self.artists_line = ""
        self.top_artists_line = ""
        self.all_tracks = []
        self.max_users = 30000

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "artists.txt"
        self.FILENAME_TOP_ARTISTS = "top_artists.txt"

        self.USER_ARTISTS_LOOP = 'user_top_artists'
        self.TOP_ARTISTS_LOOP = 'top_artists'

    def compute(self):
        tracksGen = TracksGen(True)
        tracksGen.prepare_users()

        self.all_tracks, top_tracks = tracksGen.prepare_tracks()
        self.artists_line = self.artist_array_to_line(
            "init", self.get_artist_format())
        self.top_artists_line = self.artist_array_to_line(
            "init", ['artist_ref', 'listeners', 'playcount'])
        all_artists, top_artists = self.prepare_artists()

        for idx, artist in enumerate(all_artists):
            print str(idx) + ' of ' + str(len(all_artists)) + ' ## all_artists'
            self.artists_line = self.artists_line + \
                self.artist_array_to_line(artist, self.get_artist_format())

        for idx, artist in enumerate(top_artists):
            print str(idx) + ' of ' + str(len(top_artists)) + ' ## top_artists'
            self.top_artists_line = self.top_artists_line + \
                self.artist_array_to_line(artist, ['artist_ref', 'listeners', 'playcount'])

    @staticmethod
    def get_artist_format():
        return ["name", "mbid"]

    def artist_array_to_line(self, artist="init", artist_format=[]):
        line = ""

        if artist == "":
            return ""

        for i, entry in enumerate(artist_format):
            temp_line = "%"

            if i == 0:
                temp_line = ""

            name = ""

            if artist == "init":
                name = entry
            else:
                name = re.sub(r'%*', '', artist[entry])

            line = line + temp_line + name

        return line + "\n"

    def get_artist_array(self, artist):
        name = artist['name'].encode('utf8')
        mbid = artist['mbid'].encode('utf8')

        return {
            'name': name,
            'mbid': mbid,
        }

    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.artists_line)
        to_write_file.close()


    def save_top_artists(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME_TOP_ARTISTS, 'w')

        to_write_file.write(self.top_artists_line)
        to_write_file.close()


    def prepare_artists(self):
        all_artists_dict = {}
        top_artists_dict = {}

        # loop over top artists
        files = glob(self.FETCHED_DATA + self.TOP_ARTISTS_LOOP + "/*.json")

        for idx, file in enumerate(files):
            if idx > self.max_users:
                continue

            print str(idx) + ' of ' + str(len(files)) + ' ## ' + file
            file_payload = json.load(open(file))
            artists = file_payload['artists']['artist']

            for artist in artists:
                artist_array = self.get_artist_array(artist)

                if artist_array == "":
                    continue

                top_artist = {}
                top_artist['artist_ref'] = str(len(all_artists_dict.values()))
                top_artist['listeners'] = artist['listeners']
                top_artist['playcount'] = artist['playcount']

                if not artist_array['mbid'] == '':
                    name = artist_array['mbid']
                else:
                    name = artist_array['name']

                top_artists_dict[name] = top_artist
                all_artists_dict[name] = artist_array

        # loop over users top artists
        dirs = np.array(
            glob(self.FETCHED_DATA + self.USER_ARTISTS_LOOP + "/*/"))

        for idx, user_dir in enumerate(dirs):
            if idx > self.max_users:
                continue

            files = glob(user_dir + "*.json")

            for idx_inner, file in enumerate(files):
                print str(idx) + ' of ' + str(len(dirs)) + ' ## ' + user_dir
                print str(idx_inner) + ' of ' + str(len(files)) + ' ## ' + file
                file_payload = json.load(open(file))
                artists = file_payload['topartists']['artist']

                for artist in artists:
                    artist_array = self.get_artist_array(artist)

                    if not artist_array['mbid'] == '':
                        name = artist_array['mbid']
                    else:
                        name = artist_array['name']

                    all_artists_dict[name] = artist_array


        # loop over all tracks from user
        # missing artists could be in there as well
        if self.all_tracks != []:
            for idx, track in enumerate(self.all_tracks):
                print 'Missing tracks: ' + str(idx) + ' of ' + str(len(self.all_tracks))

                if track["artist"] == "":
                    continue

                artist_array = self.get_artist_array({
                    "name": track["artist"].decode('utf8'),
                    "mbid": track["artist_mbid"].decode('utf8'),
                })

                if not artist_array['mbid'] == '':
                    name = artist_array['mbid']
                else:
                    name = artist_array['name']

                all_artists_dict[name] = artist_array

        return all_artists_dict.values(), top_artists_dict.values()


if __name__ == '__main__':
    artistGen = ArtistsGen()
    artistGen.compute()
    artistGen.save()
    artistGen.save_top_artists()
