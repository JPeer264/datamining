from glob import glob
import csv
import numpy as np
from sklearn.preprocessing import normalize
import json
import os
import scipy.sparse

from Artist import Artist
from Tracks import Tracks


class Process:
    def __init__(self):
        self.TOP_ARTISTS = "./data/top_artists.txt"
        self.USERS_TOP_ARTISTS = "./data/user_top_artists/"
        self.matrix = []
        self.useSparse = True
        self.tracks = Tracks()
        self.tracks.prepare_tracks()
        self.artists = Artist()
        self.artists.prepare_artists()

    def init(self):
        artists = []

        with open(self.TOP_ARTISTS, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                artists.append(row)

        # sort artists by playcounts
        sorted_artists = np.sort(np.array(artists).astype(int).view(
            'int,int,int'), order=['f2'], axis=0).view(np.int)[::-1]
        files = glob(self.USERS_TOP_ARTISTS + "*.txt")
        user_ids = []

        for idx, file in enumerate(files):
            add = 0

            print str(idx) + ' of ' + str(len(files))
            occurences = {}

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter='%')
                headers = reader.next()

                for row in reader:
                    user_id = row[headers.index("user_id")]

                    if add == 0:
                        user_ids.append(user_id)
                        add = 1

                    occurences[row[headers.index("artist_ref")]] = row

            if add == 0:
                continue

            line = []
            used_artists = []

            for artist in sorted_artists:
                artist_id = str(artist[0])
                used_artists.append(artist_id)
                if artist_id in occurences:
                    line.append(occurences[artist_id][3])
                else:
                    line.append(0)

            self.matrix.append(line)

        self.matrix = np.array(self.matrix)
        header = np.append('user_id', used_artists)
        print 'normalize matrix'
        normalized_matrix = normalize(self.matrix)
        print 'add left side to matrix'
        matrix_with_user_id = np.hstack(
            (np.array([user_ids]).T, normalized_matrix))
        print 'add header to matrix'
        matrix_with_header = np.append([header], matrix_with_user_id, axis=0)
        sparse_matrix = scipy.sparse.csc_matrix(normalized_matrix.astype(np.float32))

        if not os.path.exists('./data_processed'):
            os.makedirs('./data_processed')

        if self.useSparse:
            scipy.sparse.save_npz('./data_processed/top_artists-user_top_artists.npz', sparse_matrix)
            np.savetxt('./data_processed/top_artists-user_top_artists_x_labels.txt', used_artists, header='artist_ids',
                       delimiter='\t', fmt="%s")
            np.savetxt('./data_processed/top_artists-user_top_artists_y_labels.txt', user_ids, header='user_ids',
                       delimiter='\t', fmt="%s")
        else:
            np.savetxt('./data_processed/top_artists-user_top_artists.txt', matrix_with_header.astype('str'),
                   delimiter='\t', fmt="%s")


if __name__ == '__main__':
    process = Process()
    process.init()
