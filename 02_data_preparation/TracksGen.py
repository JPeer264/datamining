from glob import glob
import numpy as np
import csv
import re

try:
    import ujson as json
except ImportError:
    import json

import helper

class TracksGen:
    def __init__(self, no_artist_ref = False):
        self.tracks_line = ""
        self.top_tracks_line = ""
        self.artist_names = []
        self.artist_mbids = []
        self.no_artist_ref = no_artist_ref
        self.max_users = 30000
        self.users = []

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "tracks.txt"
        self.FILENAME_TOP_TRACKS = "top_tracks.txt"
        self.ARTISTS_FILE = self.SAVE_DIR + "artists.txt"
        self.USERS_FILE = self.SAVE_DIR + "users.txt"

        self.USER_TRACKS_LOOP = 'user_top_tracks'
        self.USERS_RECENT_TRACKS_LOOP = 'user_recent_tracks'
        self.TOP_TRACKS_LOOP = 'top_tracks'


    def compute(self):
        track_format = []
        track_format.extend(self.get_track_format())
        track_format_two = ['track_id', 'listeners', 'playcount', 'duration']
        self.prepare_users()

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


    def prepare_users(self):
        users = np.loadtxt(self.USERS_FILE, dtype='str', delimiter='\t')

        self.users = users[1:]


    def get_all_artists(self):
        artist_names = []
        artist_mbid = []

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                name = row[headers.index("name")]
                name = re.sub(r'\s*', '', name)

                artist_names.append(name)
                artist_mbid.append(row[headers.index("mbid")])

        return artist_names, artist_mbid


    def track_array_to_line(self, track="init", track_format=[]):
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


    def get_track_array(self, track):
        name = track['name']
        mbid = track['mbid']
        artist = ""

        if 'name' in track['artist']:
            artist = track['artist']['name']
        else:
            artist = track['artist']['#text']

        artist = re.sub(r'\s*', '', artist)
        artist_mbid = track['artist']['mbid']
        artist_id = ""

        if not self.no_artist_ref:
            try:
                artist_id = self.artist_mbids.index(artist_mbid)
            except ValueError:
                try:
                    artist_id = self.artist_names.index(artist)
                except ValueError:
                    pass


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
        all_tracks_dict = {}
        top_tracks_dict = {}

        # loop over top tracks
        try:
            file_payload = json.load(open(self.FETCHED_DATA + self.TOP_TRACKS_LOOP + "/" + "/page_1.json"))
            tracks = file_payload['tracks']['track']
            print str(len(tracks)) + ' tracks'

            for track in tracks:
                track_array = self.get_track_array(track)

                top_track = {}
                top_track['track_id'] = str(len(all_tracks_dict.values()))
                top_track['listeners'] = track['listeners']
                top_track['playcount'] = track['playcount']
                top_track['duration'] = track['duration']

                if not track_array['mbid'] == '':
                    name = track_array['mbid']
                else:
                    name = track_array['name']

                top_tracks_dict[name] = top_track
                all_tracks_dict[name] = track_array
        except IOError:
            print 'failed'


        # loop over user_tracks
        for idx, user in enumerate(self.users):
            if idx > self.max_users:
                continue

            print str(idx) + ' of ' + str(len(self.users)) + ' ## ' + user

            try:
                file_payload = json.load(open(self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/" + user + "/page_1.json"))
            except IOError:
                continue

            tracks = file_payload['toptracks']['track']
            print str(len(tracks)) + ' tracks'

            for track in tracks:
                track_array = self.get_track_array(track)

                if not track_array['mbid'] == '':
                    name = track_array['mbid']
                else:
                    name = track_array['name']

                all_tracks_dict[name] = track_array

        # loop over users recent tracks
        for idx, user in enumerate(self.users):
            if idx > self.max_users:
                continue

            print str(idx) + ' of ' + str(len(self.users)) + ' ## ' + user

            try:
                file_payload = json.load(open(self.FETCHED_DATA + self.USERS_RECENT_TRACKS_LOOP + "/" + user + "/page_1.json"))
            except IOError:
                continue

            tracks = file_payload['recenttracks']['track']

            for track in tracks:
                if '@attr' in track:
                    if 'nowplaying' in track['@attr']:
                        continue

                track_array = self.get_track_array(track)

                if not track_array['mbid'] == '':
                    name = track_array['mbid']
                else:
                    name = track_array['name']

                all_tracks_dict[name] = track_array

        return all_tracks_dict.values(), top_tracks_dict.values()

if __name__ == '__main__':
    tracksGen = TracksGen()
    tracksGen.compute()
    tracksGen.save()
    tracksGen.save_top_tracks()
