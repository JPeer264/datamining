from glob import glob
import numpy as np
import json
import csv

import helper


class UserRecentTracksGen:
    def __init__(self):
        self.tracks_line = ""
        self.track_names = []
        self.track_mbids = []

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/user_recent_tracks/"
        self.TRACKS_FILE = "./data/tracks.txt"

        self.USER_TRACKS_LOOP = 'user_recent_tracks'

    def compute_and_save(self):
        self.track_names, self.track_mbids = self.get_all_tracks()
        self.prepare_recent_tracks_and_save()


    @staticmethod
    def get_track_format():
        return ["track_ref"]

    def get_all_tracks(self):
        track_names = []
        track_mbids = []

        with open(self.TRACKS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                track_names.append(row[headers.index("name")])
                track_mbids.append(row[headers.index("mbid")])

        return track_names, track_mbids

    def track_array_to_line(self, track="init"):
        track_format = self.get_track_format()
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

    def get_track_array(self, track):
        name = track['name'].encode('utf8')
        mbid = track['mbid'].encode('utf8')
        track_id = ""

        # playcount = track['playcount'].encode('utf8')

        if mbid != "":
            artist_id = self.track_mbids.index(mbid)
        else:
            artist_id = self.track_names.index(name)

        self.track_names.extend([name])
        self.track_mbids.extend([mbid])

        return {
            'track_ref': str(artist_id),
        }


    def save(self, tosave, username):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + username + '.txt', 'w')

        to_write_file.write(tosave)
        to_write_file.close()

    def prepare_recent_tracks_and_save(self):
        # loop over users top tracks
        all_tracks_array = []
        dirs = np.array(
            glob(self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/*/"))

        for user_dir in dirs:
            tracks_line = self.track_array_to_line("init")
            username = user_dir.split("/")[-2]
            files = glob(user_dir + "*.json")

            for file in files:
                file_payload = json.load(open(file))
                tracks = file_payload['recenttracks']['track']

                # todo sort by timestamp
                for track in tracks:
                    if '@attr' in track:
                        if 'nowplaying' in track['@attr']:
                            continue

                    track_array = self.get_track_array(track)

                    if track_array == "":
                        continue

                    tracks_line = tracks_line + \
                        self.track_array_to_line(track_array)

            self.save(tracks_line, username)


userRecentTracksGen = UserRecentTracksGen()
userRecentTracksGen.compute_and_save()
