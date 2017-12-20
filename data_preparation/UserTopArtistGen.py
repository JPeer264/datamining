from datetime import datetime
from glob import glob
import numpy as np
import json
import csv
import re

import helper


class UserTopArtistGen:
    def __init__(self):
        self.tracks_line = ""
        self.artist_names = []
        self.artist_mbids = []
        self.user = []

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/user_top_artists/"
        self.ARTIST_FILE = "./data/artists.txt"
        self.USERS_FILE = "./data/users.txt"

        self.USER_TRACKS_LOOP = 'user_top_artists'

    def compute_and_save(self):
        self.artist_names, self.artist_mbids = self.get_all_artists()
        self.user = self.get_user_names()
        self.prepare_top_artists_and_save()

    @staticmethod
    def get_artist_format():
        return ["user_id", "artist_ref", "rank", "playcount"]

    def get_all_artists(self):
        artist_names = []
        artist_mbids = []

        with open(self.ARTIST_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                name = row[headers.index("name")]
                name = re.sub(r'\W*', '', name)

                artist_names.append(name)
                artist_mbids.append(row[headers.index("mbid")])

        return artist_names, artist_mbids

    def get_user_names(self):
        user = []

        with open(self.USERS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                name = row[headers.index("name")]

                user.append(name)

        return user

    def artist_array_to_line(self, track="init"):
        track_format = self.get_artist_format()
        line = ""

        if track == "":
            return ""

        for i, entry in enumerate(track_format):
            temp_line = "\t"

            if i == 0:
                temp_line = ""

            name = ""

            if track == "init":
                name = entry
            else:
                name = track[entry]

            line = line + temp_line + name

        return line + "\n"

    def get_artist_array(self, track, username):
        name = track['name'].encode('utf8')
        mbid = track['mbid'].encode('utf8')
        playcount = track['playcount'].encode('utf8')
        name = re.sub(r'\W*', '', name)
        rank = track['@attr']['rank'].encode('utf8')
        artist_id = ""

        if not mbid == "":
            artist_id = self.artist_mbids.index(mbid)
        else:
            artist_id = self.artist_names.index(name)

        self.artist_names.extend([name])

        if not mbid == '':
            self.artist_mbids.extend([mbid])
        else:
            self.artist_mbids.extend([name])

        return {
            'user_id': str(self.user.index(username)),
            'rank': rank,
            'playcount': playcount,
            'artist_ref': str(artist_id),
        }

    def save(self, tosave, username):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + username + '.txt', 'w')

        to_write_file.write(tosave)
        to_write_file.close()

    def prepare_top_artists_and_save(self):
        # loop over users top tracks
        dirs = np.array(
            glob(self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/*/"))

        for user_dir in dirs:
            tracks_line = self.artist_array_to_line("init")
            username = user_dir.split("/")[-2]
            files = glob(user_dir + "*.json")

            for file in files:
                file_payload = json.load(open(file))
                tracks = file_payload['topartists']['artist']

                for track in tracks:
                    track_array = self.get_artist_array(track, username)

                    if track_array == "":
                        continue

                    tracks_line = tracks_line + \
                        self.artist_array_to_line(track_array)

            self.save(tracks_line, username)


if __name__ == '__main__':
    userTopArtistGen = UserTopArtistGen()
    userTopArtistGen.compute_and_save()
