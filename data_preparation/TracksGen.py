from glob import glob
import numpy as np
import json
import csv
import re

import helper

class TracksGen:
    def __init__(self, no_artist_ref = False):
        self.tracks_line = ""
        self.top_tracks_line = ""
        self.track_names = []
        self.track_mbids = []
        self.artist_names = []
        self.artist_mbids = []
        self.no_artist_ref = no_artist_ref

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "tracks.txt"
        self.FILENAME_TOP_TRACKS = "top_tracks.txt"
        self.ARTISTS_FILE = self.SAVE_DIR + "artists.txt"

        self.USER_TRACKS_LOOP = 'user_top_tracks'
        self.USERS_RECENT_TRACKS_LOOP = 'user_recent_tracks'
        self.TOP_TRACKS_LOOP = 'top_tracks'


    def compute(self):
        track_format = []
        track_format.extend(self.get_track_format())
        track_format_two = ['track_id', 'listeners', 'playcount', 'duration']

        self.artist_names, self.artist_mbids = self.get_all_artists()
        self.tracks_line = self.track_array_to_line("init", track_format)
        self.top_tracks_line = self.track_array_to_line("init", track_format_two)
        all_tracks, top_tracks = self.prepare_tracks()

        for track in all_tracks:
            self.tracks_line = self.tracks_line + self.track_array_to_line(track, track_format)

        for track in top_tracks:
            self.top_tracks_line = self.top_tracks_line + \
                self.track_array_to_line(track, track_format_two)


    @staticmethod
    def get_track_format():
        return [ "name", "mbid", "artist_ref" ]


    def get_all_artists(self):
        artist_names = []
        artist_mbid = []

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                name = row[headers.index("name")]
                name = re.sub(r'\W*', '', name)

                artist_names.append(name)
                artist_mbid.append(row[headers.index("mbid")])

        return artist_names, artist_mbid


    def track_array_to_line(self, track="init", track_format=[]):
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
        name = track['name']
        mbid = track['mbid']
        artist = ""

        if 'name' in track['artist']:
            artist = track['artist']['name']
        else:
            artist = track['artist']['#text']

        artist = re.sub(r'\W*', '', artist)
        artist_mbid = track['artist']['mbid']
        artist_id = ""

        # playcount = track['playcount']

        # make sure the track name or mbid exists
        if ((mbid == '') and (name in self.track_names)) or (mbid in self.track_mbids):
            return ""

        if not self.no_artist_ref:
            if artist_mbid != "":
                artist_id = self.artist_mbids.index(artist_mbid)
            else:
                artist_id = self.artist_names.index(artist)

        self.track_names.extend([name])

        if not mbid == '':
            self.track_mbids.extend([mbid])
        else:
            self.track_mbids.extend([name])

        return {
            'name': name.encode('utf8'),
            'mbid': mbid.encode('utf8'),
            'artist': artist.encode('utf8'),
            'artist_mbid': artist_mbid.encode('utf8'),
            'artist_ref': str(artist_id).encode('utf8'),
        }


    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.tracks_line)
        to_write_file.close()

    def save_top_tracks(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME_TOP_TRACKS, 'w')

        to_write_file.write(self.top_tracks_line)
        to_write_file.close()


    def prepare_tracks(self):
        # loop over users top tracks
        all_tracks_array = []
        top_tracks_array = []

        # loop over top tracks
        files = glob(self.FETCHED_DATA + self.TOP_TRACKS_LOOP + "/*.json")

        for idx, file in enumerate(files):
            print str(idx) + ' of ' + str(len(files)) + ' ## ' + file
            file_payload = json.load(open(file))
            tracks = file_payload['tracks']['track']

            for track in tracks:
                track_array = self.get_track_array(track)

                if track_array == "":
                    continue

                top_track = {}
                top_track['track_id'] = str(len(all_tracks_array))
                top_track['listeners'] = track['listeners']
                top_track['playcount'] = track['playcount']
                top_track['duration'] = track['duration']
                top_tracks_array.extend([top_track])
                all_tracks_array.extend([track_array])

        # loop over user_tracks
        dirs = np.array(glob(self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/*/"))

        for idx, user_dir in enumerate(dirs):
            files = glob(user_dir + "*.json")

            for idx_inner, file in enumerate(files):
                print str(idx) + ' of ' + str(len(dirs)) + ' ## ' + user_dir
                print str(idx_inner) + ' of ' + str(len(files)) + ' ## ' + file
                file_payload = json.load(open(file))
                tracks = file_payload['toptracks']['track']

                for track in tracks:
                    track_array = self.get_track_array(track)

                    if track_array == "":
                        continue

                    all_tracks_array.extend([track_array])

            files = glob(user_dir + "*.json")

        # loop over users recent tracks
        dirs = np.array(glob(self.FETCHED_DATA + self.USERS_RECENT_TRACKS_LOOP + "/*/"))

        for idx, user_dir in enumerate(dirs):
            files = glob(user_dir + "*.json")
            for idx_inner, file in enumerate(files):
                print str(idx) + ' of ' + str(len(dirs)) + ' ## ' + user_dir
                print str(idx_inner) + ' of ' + str(len(files)) + ' ## ' + file
                file_payload = json.load(open(file))
                tracks = file_payload['recenttracks']['track']

                for track in tracks:
                    if '@attr' in track:
                        if 'nowplaying' in track['@attr']:
                            continue

                    track_array = self.get_track_array(track)

                    if track_array == "":
                        continue

                    all_tracks_array.extend([track_array])

        return all_tracks_array, top_tracks_array

if __name__ == '__main__':
    tracksGen = TracksGen()
    tracksGen.compute()
    tracksGen.save()
    tracksGen.save_top_tracks()
