import argparse
import os
import time
import numpy as np
import sys
from multiprocessing import Process, JoinableQueue
from ctypes import *
from scipy.sparse import coo_matrix, load_npz

GRAPH_FILE = os.environ.get("GRAPH_FILE", "graph.npz")
OUT_FILE = os.environ.get("OUT_FILE", "/apsp/apsp.npy")

INF = 2**31 - 1


def parse_args():
    parser = argparse.ArgumentParser(description='Build APSP matrix')
    parser.add_argument('--limit', default=None, type=int,
                        help='Maximum number of nodes to process')
    parser.add_argument('--offset', default=0, type=int,
                        help='First node to process from')
    parser.add_argument('--build', default=False,
                        action='store_const', const=True,
                        help='Whether or not to build the matrix from the partial file')

    return parser.parse_args()


def write(fh, q):
    while True:
        msg = q.get()
        if msg == 'DONE':
            q.task_done()
            break
        else:
            for i, j, v in msg:
                fh.write('{},{},{}\n'.format(i, j, v))
            q.task_done()


if __name__ == '__main__':
    args = parse_args()

    graph = load_npz(GRAPH_FILE)
    gunrock = cdll.LoadLibrary('/gunrock/build/lib/libgunrock.so')

    # input
    col = pointer((c_int * len(graph.indices))(*graph.indices))
    row = pointer((c_int * len(graph.indptr))(*graph.indptr))
    val = pointer((c_uint * len(graph.data))(*graph.data))
    nodes = len(graph.indptr) - 1
    edges = len(graph.indices)

    # output
    labels = pointer((c_uint * nodes)())
    preds = pointer((c_uint * nodes)())

    durations = []
    offset = args.offset
    limit = args.limit or nodes

    partial_file = '{}.partial'.format(OUT_FILE)
    if os.path.exists(partial_file):
        pass
        # print('Existing partial file {} found'.format(partial_file))
        # exit(1)

    with open(partial_file, 'a') as fh:
        q = JoinableQueue()
        p = Process(target=write, args=(fh, q))
        p.start()
        for i in range(offset, min(offset+limit, nodes)):
            start = time.time()
            # source node
            sources = pointer((c_uint * 1)(i))

            gunrock.sssp(labels, preds, nodes, edges,
                         row, col, val, 1, sources, 0)

            out_triplets = [(int(i), int(j), int(v))
                            for j, v in enumerate(labels[0]) if v < INF]
            q.put(out_triplets)

            durations = [time.time() - start] + durations[:99]
            print(
                'Processed:', i,
                'out of:', nodes,
                'avg time/node:', np.mean(durations)
            )

        q.put('DONE')

        print('Emptying queue')
        q.join()
        p.join()

    if args.build:
        print('Allocating matrix')
        out = np.zeros(np.shape(graph), dtype=np.uint8)
        print('Reading matrix values')
        with open(partial_file, 'r') as fh:
            for line_num, line in enumerate(fh):
                stripped = line[:-1]
                i, j, v = stripped.split(',')
                out[int(i), int(j)] = int(v)
                if line_num % 10000000 == 0:
                    print('Finished {}'.format(line_num))
        print('Saving matrix')
        np.save(OUT_FILE, out)
