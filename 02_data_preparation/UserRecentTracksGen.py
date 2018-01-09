from datetime import datetime
from glob import glob
import numpy as np
import json
import csv
import re

import helper
from TracksGen import TracksGen

class UserRecentTracksGen:
    def __init__(self):
        self.tracks_line = ""
        self.track_names = []
        self.track_mbids = []
        self.user = []
        self.max_users = 40000

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/user_recent_tracks/"
        self.TRACKS_FILE = "./data/tracks.txt"
        self.USERS_FILE = "./data/users.txt"

        self.USER_TRACKS_LOOP = 'user_recent_tracks'

    def compute_and_save(self):
        self.track_names, self.track_mbids = self.get_all_tracks()
        self.user = self.get_user_names()
        self.prepare_recent_tracks_and_save()


    @staticmethod
    def get_track_format():
        return ["user_id", "uts", "track_ref"]


    def get_all_tracks(self):
        track_names = {}
        track_mbids = {}

        with open(self.TRACKS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()[0].split(' ')

            counter = 0

            for row in reader:
                name = row[headers.index("name")]
                name = re.sub(r'\s*', '', name)
                mbid = row[headers.index("mbid")]

                if not mbid == "":
                    track_mbids[row[headers.index("mbid")]] = counter

                track_names[name] = counter
                counter += 1

        return track_names, track_mbids


    def get_user_names(self):
        user = []

        with open(self.USERS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                name = row[headers.index("name")]

                user.append(name)

        return user


    def track_array_to_line(self, track="init"):
        track_format = self.get_track_format()
        line = ""

        if track == "":
            return ""

        for i, entry in enumerate(track_format):
            temp_line = "%"

            if i == 0:
                temp_line = ""

            name = ""

            if track == "init":
                name = entry
            else:
                name = re.sub(r'%*', '', track[entry])

            line = line + temp_line + name

        return line + "\n"


    def get_track_array(self, track, username):
        name = track['name'].encode('utf8')
        mbid = track['mbid'].encode('utf8')
        name = re.sub(r'\s*', '', name)
        uts = track['date']['uts'].encode('utf8')
        track_id = ""

        try:
            track_id = self.track_mbids[mbid]
        except KeyError:
            try:
                track_id = self.track_names[name]
            except KeyError:
                pass

        return {
            'user_id': str(self.user.index(username)),
            'uts': uts,
            'track_ref': str(track_id),
        }


    def save(self, tosave, username):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + username + '.txt', 'w')

        to_write_file.write(tosave)
        to_write_file.close()


    def prepare_recent_tracks_and_save(self):
        # loop over users top tracks
        all_tracks_array = []

        for idx, user in enumerate(self.user):
            if idx > self.max_users:
                continue

            print str(idx) + ' of ' + str(len(self.user)) + " ## " + user
            tracks_line = self.track_array_to_line("init")
            user_dir = self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/" + user
            files = glob(user_dir + "/*.json")
            all_tracks = []

            for file in files:
                file_payload = json.load(open(file))
                tracks = file_payload['recenttracks']['track']

                for track in tracks:
                    if '@attr' in track:
                        if 'nowplaying' in track['@attr']:
                            continue

                    if not 'name' in track:
                        continue

                    all_tracks.append(track)

            # sort by timestamp
            all_tracks.sort(
                key=lambda x: datetime.strptime(x['date']['#text'], '%d %b %Y, %H:%M'),
                reverse=True,
            )

            for track in all_tracks:
                track_array = self.get_track_array(track, user)

                tracks_line = tracks_line + \
                    self.track_array_to_line(track_array)

            self.save(tracks_line, user)


if __name__ == '__main__':
    userRecentTracksGen = UserRecentTracksGen()
    userRecentTracksGen.compute_and_save()
