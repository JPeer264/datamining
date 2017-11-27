from glob import glob
import numpy as np
import json

import helper

FETCHED_DATA = "./fetched_data/"
SAVE_DIR = "./data/"
FILENAME = "tracks.txt"

USER_TRACKS_LOOP = 'user_top_tracks'
TOP_TRACKS_LOOP = 'top_tracks'

def prepare_tracks():
    # loop over users top tracks
    dirs = np.array(glob(FETCHED_DATA + USER_TRACKS_LOOP + "/*/"))
    tracks_line = "name\tmbid\tartist\tartist_mbid\n"
    track_names = []
    track_mbid = []

    for user_dir in dirs:
        files = glob(user_dir + "*.json")

        for file in files:
            file_payload = json.load(open(file))
            tracks = file_payload['toptracks']['track']

            for track in tracks:
                name = track['name'].encode('utf8')
                mbid = track['mbid'].encode('utf8')
                artist = track['artist']['name'].encode('utf8')
                artist_mbid = track['artist']['mbid'].encode('utf8')

                # playcount = track['playcount'].encode('utf8')

                # make sure the track name or mbid exists
                if ((mbid == '') & (name in track_names)) | (mbid in track_mbid):
                    continue

                track_names.extend([name])
                track_mbid.extend([mbid])

                tracks_line = tracks_line + "{name}\t{mbid}\t{artist}\t{artist_mbid}\n".format(
                    name=name,
                    mbid=mbid,
                    artist=artist,
                    artist_mbid=artist_mbid
                )

    file = open(SAVE_DIR + FILENAME, 'w')

    file.write(tracks_line)
    file.close()


prepare_tracks()
