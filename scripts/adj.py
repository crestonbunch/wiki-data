import argparse
import requests
import json
import time
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from scipy.sparse import coo_matrix, csr_matrix, save_npz
from scipy.sparse.csgraph import floyd_warshall
from neo4j.v1 import GraphDatabase

GRAPH_QUERY = '''
MATCH (p0:Page {artist: true}) -[:Link]-> (p:Page {artist: true})
RETURN p0, p
'''


def parse_args():
    parser = argparse.ArgumentParser(
        description='Build the graph adjacency matrix')
    parser.add_argument('--neo4j_host', default='bolt://localhost',
                        help='Neo4j host, default \'bolt://localhost\'')
    parser.add_argument('--neo4j_user', default='neo4j',
                        help='Neo4j username, default \'neo4j\'')
    parser.add_argument('--neo4j_pw', help='Neo4j password')
    parser.add_argument('--infile', default='artists.txt',
                        help='List of artist wikipedia pages')
    parser.add_argument('--outfile', default='graph.npz',
                        help='File to output graph distance matrix to')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    n4j = GraphDatabase.driver(
        args.neo4j_host, auth=(args.neo4j_user, args.neo4j_pw))

    with open(args.infile, 'r') as fh:
        artists = fh.read().strip().split('\n')
        artist_indices = {artist: i for i, artist in enumerate(artists)}

    # adj_matrix = csr_matrix((len(artists), len(artists)))
    # adj_matrix = np.zeros((len(artists), len(artists)))
    rows, cols, vals = [], [], []

    print('Querying edges')
    with open(args.outfile, 'a') as fh:
        with n4j.session() as session:
            edges = session.run(GRAPH_QUERY)
            print('Building adjacency matrix')
            for edge in edges:
                row_title = edge['p0']['title']
                col_title = edge['p']['title']
                rows.append(artist_indices[row_title])
                cols.append(artist_indices[col_title])
                vals.append(1)
                # row, col = artist_indices[row_title], artist_indices[col_title]
                # adj_matrix[row, col] = 1
    n4j.close()

    adj_matrix = coo_matrix((vals, (rows, cols)),
                            shape=(len(artists), len(artists)))
    print('Converting to CSR')
    adj_matrix = adj_matrix.tocsr()

    print('Saving')
    save_npz(args.outfile, adj_matrix)
