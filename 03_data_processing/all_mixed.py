from glob import glob
import csv
import numpy as np
from sklearn.preprocessing import normalize
import json
import os
import os.path
import scipy.sparse

from Artist import Artist
from Tracks import Tracks


class Process:
    def __init__(self):
        self.DATA = './data/'
        self.USERS_TOP_TRACKS = self.DATA + "user_top_tracks/"
        self.USERS_RECENT_TRACKS = self.DATA + "user_recent_tracks/"
        self.matrix = []
        self.useSparse = False

        self.tracks = Tracks()
        self.tracks.prepare_tracks()


    def init(self):
        top_tracks_files = glob(self.USERS_TOP_TRACKS + "*.txt")
        user_ids = []

        for idx, file in enumerate(top_tracks_files):
            # if idx > 10:
            #     continue
            print str(idx) + ' of ' + str(len(top_tracks_files))
            add = 0
            add2 = 0
            top_tracks = []
            occurences = []
            occured_artists = []
            usertxt = file.split("/")[-1]

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter='%')
                headers = reader.next()

                for row in reader:
                    user_id = row[headers.index("user_id")]
                    track_ref = row[headers.index("track_ref")]

                    if add == 0:
                        this_user_id = user_id
                        add = 1

                    if track_ref == '':
                        top_tracks.append([row[1], row[2], '-1'])
                        continue

                    top_tracks.append(row[1:])

            with open(self.USERS_RECENT_TRACKS + usertxt) as f:
                reader = csv.reader(f, delimiter='%')
                headers = reader.next()

                for row in reader:
                    if add2 == 0:
                        add2 = 1

                    track_id = row[headers.index("track_ref")]

                    occurences.append(track_id)
                    occured_artists.append(self.tracks.get_artist(track_id))

            if (add == 0) or (add2 == 0):
                continue

            user_ids.append(this_user_id)
            unique, counts = np.unique(np.array(occurences), return_counts=True)
            unique_artists = np.unique(np.array(occured_artists))
            zipped_counts = dict(zip(unique, counts))

            known_songs = 0
            different_songs = len(counts)
            different_artists = len(unique_artists)

            if '-1' in unique_artists:
                different_artists = different_artists - 1

            for track in top_tracks:
                track_id = str(track[-1])

                if track_id in zipped_counts:
                    known_songs += zipped_counts[track_id]
                    zipped_counts.pop(track_id, None)

            new_songs = sum(zipped_counts.values())

            self.matrix.append(
                [known_songs, new_songs, different_songs, different_artists])

        self.matrix = np.array(self.matrix)
        header = np.append('user_id', np.arange(len(self.matrix)) + 1)
        normalized_matrix = normalize(self.matrix)

        if not os.path.exists('./data_processed'):
            os.makedirs('./data_processed')

        if self.useSparse:
            sparse_matrix = scipy.sparse.csc_matrix(normalized_matrix)
            scipy.sparse.save_npz(
                './data_processed/all_mixed.npz', sparse_matrix)
            np.savetxt('./data_processed/all_mixed_x_labels.txt', ['known_songs', 'new_songs', 'different_songs', 'different_artists'], header='labels',
                       delimiter='\t', fmt="%s")
            np.savetxt('./data_processed/all_mixed_y_labels.txt', user_ids, header='user_ids',
                       delimiter='\t', fmt="%s")
        else:
            # matrix_with_user_id = np.hstack(
            #     (np.array([user_ids]).T, normalized_matrix))
            # matrix_with_header = np.append([header], matrix_with_user_id, axis=0)
            np.savetxt('./data_processed/all_mixed.txt', normalized_matrix.astype(np.float),
                       delimiter='\t', fmt="%s")


if __name__ == '__main__':
    process = Process()
    process.init()
