from glob import glob
import csv
import numpy as np
from sklearn.preprocessing import normalize
import json
import os

from Artist import Artist
from Tracks import Tracks


class Process:
    def __init__(self):
        self.TOP_TAGS = "./data/top_tags.txt"
        self.USERS_TOP_ARTISTS = "./data/user_top_artists/"
        self.matrix = np.array([])
        self.tracks = Tracks()
        self.tracks.prepare_tracks()
        self.artists = Artist()
        self.artists.prepare_artists()


    def init(self):
        tags = []

        with open(self.TOP_TAGS, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()

            for row in reader:
                tags.append(row)

        # sort tags by reach
        sorted_tags = np.sort(np.array(tags).astype(int).view(
            'int,int,int'), order=['f1'], axis=0).view(np.int)[::-1]
        a = sorted_tags.astype('str')

        files = glob(self.USERS_TOP_ARTISTS + "*.txt")
        user_ids = []

        for file in files:
            occurences = []

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                headers = reader.next()

                for row in reader:
                    user_id = row[headers.index("user_id")]

                    if not user_id in user_ids:
                        user_ids.append(user_id)

                    artist_tags = self.artists.get_artist_tags(row[headers.index("artist_ref")])
                    occurences.extend(artist_tags)

            unique, counts = np.unique(np.array(occurences), return_counts=True)
            zipped_counts = dict(zip(unique, counts))

            line = []
            used_tags = []

            for tag in sorted_tags:
                tag_id = str(tag[0])
                used_tags.append(tag_id)
                if tag_id in zipped_counts:
                    line.append(zipped_counts[tag_id])
                else:
                    line.append(0)

            if len(self.matrix) == 0:
                self.matrix = np.array([line])
            else:
                self.matrix = np.append(self.matrix, [line], axis=0)

        header = np.append('user_id', used_tags)
        normalized_matrix = normalize(self.matrix)
        matrix_with_user_id = np.hstack((np.array([user_ids]).T, normalized_matrix))
        matrix_with_header = np.append([header], matrix_with_user_id, axis=0)

        if not os.path.exists('./data_processed'):
            os.makedirs('./data_processed')

        np.savetxt('./data_processed/top_tags-user_top_artists.txt', matrix_with_header.astype('str'),
                   delimiter='\t', fmt="%s")


if __name__ == '__main__':
    process = Process()
    process.init()
