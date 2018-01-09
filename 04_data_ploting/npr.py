import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os
import scipy.sparse
from sklearn.decomposition import PCA
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.cluster import KMeans
import sklearn.metrics.pairwise as pair_dist


class NPR:
    def __init__(self, file_name='user_top_tracks-user_recent_tracks.txt'):
        self.DATA_DIR = './data_processed/'
        self.FEATURES_FILE = self.DATA_DIR + file_name
        self.OUTPUT_VISU_DIR = './visualizations/'


    @staticmethod
    def transform_tsne(perp=20.0):
        tsne = TSNE(
            n_components=2,
            verbose=1,
            perplexity=perp,
            early_exaggeration=12.0,
            learning_rate=200.0,
            n_iter=1000,
            n_iter_without_progress=300,
            min_grad_norm=1e-07,
            metric='euclidean',
            init='random',
            random_state=None,
            method='barnes_hut',
            angle=0.5
        )

        return tsne


    @staticmethod
    def transform_mds():
        mds = MDS(
            n_components=2,
            verbose=1,
            dissimilarity='euclidean'
        )

        return mds

    @staticmethod
    def transform_lle():
        lle = LocallyLinearEmbedding(
            n_components=2,
            n_jobs=2,
            verbose=1,
        )

        return lle


    @staticmethod
    def transform_lda():
        lda = LatentDirichletAllocation(
            n_jobs=2,
            verbose=1,
        )

        return lda


    @staticmethod
    def compute_NPR(P, D, nn):
        # Return -1 if size of P and D is different
        if P.shape != D.shape:
            return -1

        npr = 0
        # For all data points
        for i in range(0, P.shape[0]):
            idx_sorted_P = np.argsort(P[i])
            idx_sorted_D = np.argsort(D[i])
            nn_P = idx_sorted_P[1:nn + 1] # Get nn nearest items to P_i
            nn_D = idx_sorted_D[1:nn + 1] # Get nn nearest items to D_i

            # Compute NPR for current data point
            npr_i = len(np.intersect1d(nn_P, nn_D)) / np.float32(nn)
            npr = npr + npr_i / P.shape[0]

        return npr


    def show_npr(self):
        for nn in [1, 3, 5, 10, 25, 50]:
            print 'NPR(nn=%d): %.3f%%' % (nn, self.compute_NPR(pair_dist.euclidean_distances(self.data), pair_dist.euclidean_distances(self.Y), nn) * 100.0)


    def read_data(self):
        filename, file_extension = os.path.splitext(self.FEATURES_FILE)

        if file_extension == '.txt':
            raw_data = np.loadtxt(self.FEATURES_FILE,
                                  dtype='str', delimiter='\t')

            self.labels = raw_data[1:, 0]
            self.header = raw_data[0, 1:]
            self.data = np.delete(np.delete(raw_data, 0, 0), 0, 1).astype(
                np.float)  # remove header, and left column
        else:
            self.labels = np.loadtxt(filename + "_y_labels.txt").astype('int')
            self.header = np.loadtxt(filename + "_x_labels.txt").astype('int')
            self.data = scipy.sparse.load_npz(filename + ".npz").todense()


    def no_train(self):
        self.read_data()
        self.Y = self.data


    def train(self, method='tsne'):
        self.read_data()
        self.method = method

        algo = {
            'tsne': self.transform_tsne,
            'mds': self.transform_mds,
            'lle': self.transform_lle,
            'lda': self.transform_lda,
        }

        computed_algo = algo[method]()

        self.Y = computed_algo.fit_transform(self.data)
        self.algo = computed_algo


    def plot(self, labels=[]):
        plt.figure(figsize=(11.69, 8.27))

        if not labels == []:
            self.labels = labels

        # Plot results
        if not self.labels == []:        # If we have labels, print data items with same label in same color
            # Define color space
            colors = iter(cm.rainbow(np.linspace(0, 1, len(np.unique(self.labels)))))
            for l in np.unique(self.labels):
                # Identify indices with matching labels
                idx = np.where(self.labels == l)
                # Next color for every new class/label
                c = next(colors)
                plt.scatter(self.Y[idx, 0], self.Y[idx, 1], color=c)      # Add scatter plot
        else:                       # No labels -> all data points in same color
            plt.scatter(self.Y[:, 0], self.Y[:, 1], color='b')
            #OR: plt.plot(Y[:, 0], Y[:, 1], 'o', color='r')

        # Add title and legend
        plt.title(self.method)
        plt.legend(fontsize=8)
        # Save as PDF (without axes and grid)
        plt.axis('off')
        plt.grid(False)
        plt.tight_layout()
        # plt.savefig(OUTPUT_VISU_DIR + method + '.pdf', format='pdf', dpi=300)
        # plt.close()
        plt.show()


if __name__ == '__main__':
    npr = NPR()
    npr.train('mds')
    # kmeans = KMeans(n_clusters=15).fit(npr.Y)
    # npr.show_npr()
    npr.plot()

    # test = npr.algo.fit(npr.Y)
    print ''
