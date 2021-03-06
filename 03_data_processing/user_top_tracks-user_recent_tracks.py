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

            if len(top_tracks) < 200:
                continue


            # todo rank sort by rank
            sorted_top_tracks = np.sort(np.array(top_tracks).astype(int).view(
                'int,int,int'), order=['f1'], axis=0).view(np.int).astype('str')

            with open (self.USERS_RECENT_TRACKS + usertxt) as f:
                reader = csv.reader(f, delimiter='%')
                headers = reader.next()

                for row in reader:
                    if add2 == 0:
                        add2 = 1

                    occurences.append(row[headers.index("track_ref")])

            if (add == 0) or (add2 == 0):
                continue

            user_ids.append(this_user_id)
            unique, counts = np.unique(
                np.array(occurences), return_counts=True)
            zipped_counts = dict(zip(unique, counts))

            line = []

            for track in sorted_top_tracks:
                track_id = str(track[-1])

                if track_id in zipped_counts:
                    line.append(zipped_counts[track_id])
                else:
                    line.append(0)

            self.matrix.append(line[0:200])

        self.matrix = np.array(self.matrix)
        header = np.append('user_id', np.arange(len(self.matrix)) + 1)
        normalized_matrix = normalize(self.matrix)

        if not os.path.exists('./data_processed'):
            os.makedirs('./data_processed')

        if self.useSparse:
            sparse_matrix = scipy.sparse.csc_matrix(normalized_matrix)
            scipy.sparse.save_npz(
                './data_processed/user_top_tracks-user_recent_tracks.npz', sparse_matrix)
            np.savetxt('./data_processed/user_top_tracks-user_recent_tracks_x_labels.txt', np.arange(len(self.matrix)) + 1, header='ranks',
                       delimiter='\t', fmt="%s")
            np.savetxt('./data_processed/user_top_tracks-user_recent_tracks_y_labels.txt', user_ids, header='user_ids',
                       delimiter='\t', fmt="%s")
        else:
            # matrix_with_user_id = np.hstack(
            #     (np.array([user_ids]).T, normalized_matrix))
            # matrix_with_header = np.append([header], matrix_with_user_id, axis=0)
            np.savetxt('./data_processed/user_top_tracks-user_recent_tracks.txt', normalized_matrix.astype(np.float),
                    delimiter='\t', fmt="%s")


if __name__ == '__main__':
    process = Process()
    process.init()
