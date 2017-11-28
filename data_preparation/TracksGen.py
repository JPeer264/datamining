from glob import glob
import numpy as np
import json
import csv

import helper

class TracksGen:
    def __init__(self):
        self.tracks_line = ""
        self.track_names = []
        self.track_mbids = []
        self.artist_names = []
        self.artist_mbids = []

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "tracks.txt"
        self.ARTISTS_FILE = self.SAVE_DIR + "/artists.txt"

        self.USER_TRACKS_LOOP = 'user_top_tracks'
        self.TOP_TRACKS_LOOP = 'top_tracks'


    def compute(self):
        self.artist_names, self.artist_mbids = self.get_all_artists()
        self.tracks_line = self.track_array_to_line("init")
        all_tracks = self.prepare_tracks()

        for track in all_tracks:
            self.tracks_line = self.tracks_line + self.track_array_to_line(track)


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
                artist_names.append(row[headers.index("name")])
                artist_mbid.append(row[headers.index("mbid")])

        return artist_names, artist_mbid


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
        artist = track['artist']['name'].encode('utf8')
        artist_mbid = track['artist']['mbid'].encode('utf8')
        artist_id = ""

        # playcount = track['playcount'].encode('utf8')

        # make sure the track name or mbid exists
        if ((mbid == '') & (name in self.track_names)) | (mbid in self.track_mbids):
            return ""

        if artist_mbid != "":
            artist_id = self.artist_mbids.index(artist_mbid)
        else:
            artist_id = self.artist_names.index(artist)

        self.track_names.extend([name])
        self.track_mbids.extend([mbid])

        return {
            'name': name,
            'mbid': mbid,
            'artist_ref': str(artist_id),
        }


    def save(self):
        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.tracks_line)
        to_write_file.close()


    def prepare_tracks(self):
        # loop over users top tracks
        all_tracks_array = []
        dirs = np.array(glob(self.FETCHED_DATA + self.USER_TRACKS_LOOP + "/*/"))

        for user_dir in dirs:
            files = glob(user_dir + "*.json")

            for file in files:
                file_payload = json.load(open(file))
                tracks = file_payload['toptracks']['track']

                for track in tracks:
                    track_array = self.get_track_array(track)

                    if track_array == "":
                        continue

                    all_tracks_array.extend([track_array])

        # loop over top tracks
        files = glob(self.FETCHED_DATA + self.TOP_TRACKS_LOOP + "/*.json")

        for file in files:
            file_payload = json.load(open(file))
            tracks = file_payload['tracks']['track']

            for track in tracks:
                track_array = self.get_track_array(track)

                if track_array == "":
                    continue

                all_tracks_array.extend([track_array])

        return all_tracks_array


a = TracksGen()
a.compute()
a.save()
