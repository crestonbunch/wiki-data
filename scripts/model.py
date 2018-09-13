import argparse
import requests
import json
import time
import numpy as np
# import pycuda.autoinit
# import pycuda.gpuarray as gpuarray
# from skcuda.linalg import PCA
from sklearn.decomposition import IncrementalPCA
from sklearn.random_projection import SparseRandomProjection
from sklearn.externals import joblib


def parse_args():
    parser = argparse.ArgumentParser(
        description='Tag wikipedia article names with artist names')
    parser.add_argument('--infile', default='apsp.npy',
                        help='APSP matrix')
    parser.add_argument('--outfile', default='model.pkl',
                        help='Model save file')
    parser.add_argument('--num_components', default=100, type=int,
                        help='Number latent topics in the model')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    model = IncrementalPCA(n_components=args.num_components)

    apsp = np.load(args.infile)
    # apsp_gpu = gpuarray.GPUArray(np.shape(apsp), np.float32, order="F")
    # apsp_gpu.set(apsp)

    print('Fitting model')
    # model = model.fit_transform(apsp_gpu)
    model = model.fit_transform(apsp)

    print('Saving model')
    joblib.dump(model, args.outfile)
