import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os
import sompy
from sompy.visualization.mapview import View2D
from sompy.visualization.bmuhits import BmuHitsView
from sompy.visualization.hitmap import HitMapView


class SOM:
    def __init__(self, file_name='top_tags-user_top_artists.txt'):
        self.DATA_DIR = './data_processed/'
        self.FEATURES_FILE = self.DATA_DIR + file_name
        self.OUTPUT_VISU_DIR = './visualizations/'


    def train(self):
        data = np.loadtxt(self.FEATURES_FILE, dtype='str', delimiter='\t')
        user_ids = data[1:, 0]
        tags = data[0, 1:]
        new_data = np.delete(np.delete(data, 0, 0), 0, 1).astype(np.float) # remove header, and left column

        map_size = [8, 12]
        # Init and train SOM
        som = sompy.SOMFactory.build(
            new_data,
            map_size,
            mask=None,
            mapshape='planar',
            lattice='rect',
            normalization='var',
            initialization='pca',
            neighborhood='gaussian',
            training='batch',
            name='SOM'
        )

        som.train(n_job=4, verbose='debug', train_rough_len=3, train_finetune_len=10)

        self.som = som


    def show_error(self):
        topographic_error = self.som.calculate_topographic_error()
        # som._bmu[1] contains quantization errors for all map units
        quantization_error = np.mean(self.som._bmu[1])
        print 'Topographic error = %s, Quantization error = %s' % (topographic_error, quantization_error)


    def plot_umatrix(self):
        u = sompy.umatrix.UMatrixView(
            50,
            50,
            'U-matrix',
            show_axis=True,
            text_size=12,
            show_text=True
        )

        # Compute U-matrix values
        u.build_u_matrix(self.som, distance=1, row_normalized=False)

        u.show(
            self.som,
            row_normalized=False,
            show_data=True,
            contooor=False,
            blob=False
        )


    def plot_hitmap(self):
        hv = BmuHitsView(2, 2, 'Hit Map', text_size=12)
        hv.show(
            self.som,
            anotate=True,
            onlyzeros=False,
            labelsize=12,
            cmap="Greys",
            logaritmic=False
        )


    def plot_kmeans(self):
        self.som.cluster(n_clusters=16)

        hits = HitMapView(6, 6, 'K-means Clustering', text_size=12)

        hits.show(self.som)


if __name__ == '__main__':
    som = SOM()
    som.train()
    som.plot_umatrix()
    som.plot_hitmap()
    som.plot_kmeans()
