import argparse
import codecs
import numpy as np
from scipy.spatial.distance import cosine, euclidean


def parse_args():
    parser = argparse.ArgumentParser(
        description='Find artist recommendations using cosine distance')
    parser.add_argument('page_name', help='Input Wikipedia page title')
    parser.add_argument('--infile', default='apsp.npy',
                        help='APSP matrix')
    parser.add_argument('--artistsfile', default='artists.txt',
                        help='Artists file')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    artists = codecs.open(args.artistsfile).read().split('\n')
    apsp = np.load(args.infile)

    index = artists.index(args.page_name)

    vector = apsp[index]
    print(np.shape(vector))

    rankings = []
    for i, other in enumerate(apsp):
        if i == index:
            continue
        distance = cosine(vector, other)
        rankings.append((distance, i))
        if i % 1000 == 0:
            print('{}/{}'.format(i, len(artists)), end='\r')
    print()

    sort = list(sorted(rankings))
    for distance, i in sort[:10]:
        artist = artists[i]
        print('{:.3E} {}'.format(distance, artist))
