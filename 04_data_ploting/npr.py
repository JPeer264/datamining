import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import sklearn.metrics.pairwise as pair_dist


class NPR:
    def __init__(self, file_name='top_tags-user_top_artists.txt'):
        self.DATA_DIR = './data_processed/'
        self.FEATURES_FILE = self.DATA_DIR + file_name
        self.OUTPUT_VISU_DIR = './visualizations/'


    def train(self):
        raw_data = np.loadtxt(self.FEATURES_FILE, dtype='str', delimiter='\t')

        self.labels = raw_data[1:, 0]
        self.header = raw_data[0, 1:]
        self.data = np.delete(np.delete(raw_data, 0, 0), 0, 1).astype(np.float)  # remove header, and left column

        perp = 10.0
        tsne = TSNE(
            n_components=2,
            verbose=0,
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

        self.Y = tsne.fit_transform(self.data)


    def plot_tsne(self):
        plt.figure(figsize=(11.69, 8.27))

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
        plt.title('T-SNE')
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
    npr.train()
    npr.plot_tsne()
