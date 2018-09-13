import argparse
import numpy as np
import tensorflow as tf
import time
from math import ceil


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate a lower dimensional matrix')
    parser.add_argument('--infile', default='apsp.npy',
                        help='APSP matrix')
    parser.add_argument('--outfile', default='compressed.npy',
                        help='Compressed vectors output matrix')
    parser.add_argument('--dims', default=100, type=int,
                        help='Number of dimensions in the output vectors')
    parser.add_argument('--batch_size', default=100, type=int,
                        help='Number of nodes to process each iteration')
    parser.add_argument('--epochs', default=10, type=int,
                        help='Number of epochs to run')

    return parser.parse_args()


def gen_inputs(matrix):
    return (
        (i, j, matrix[i, j])
        for i in range(matrix.shape[0])
        for j in range(matrix.shape[1])
    )


def num_inputs(matrix):
    return matrix.shape[0] * matrix.shape[1]


if __name__ == '__main__':
    args = parse_args()

    apsp = np.load(args.infile)
    num_labels = np.amax(apsp)

    vec_input = tf.placeholder(tf.float32, (None, apsp.shape[1]))
    normalized_input = tf.nn.l2_normalize(vec_input)

    compressor = tf.layers.Dense(args.dims, activation=tf.nn.sigmoid)
    decompressor = tf.layers.Dense(apsp.shape[1], activation=tf.nn.sigmoid)
    # learn the identity function by projecting into a smaller space and then
    # projecting back to the original space
    compressed = compressor(normalized_input)
    decompressed = decompressor(compressed)
    loss = tf.losses.mean_squared_error(normalized_input, decompressed)

    global_step = tf.Variable(0, name='global_step', trainable=False)
    learning_rate = 0.001
    train_step = tf.contrib.layers.optimize_loss(
        loss,
        global_step,
        learning_rate,
        'Adam',
        summaries=[]
    )
    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init_op)

        losses = []
        msg = 'Epoch: {}/{}, Processed: {}/{}, Avg loss {:.5f} in {:.3f}s'
        try:
            for i in range(1, args.epochs):
                start = time.time()
                for j in range(0, apsp.shape[0], args.batch_size):
                    batch = apsp[j:j+args.batch_size]
                    err, _ = sess.run(
                        [loss, train_step],
                        feed_dict={vec_input: batch}
                    )
                    losses.append(err)
                    if j % 1000 == 0:
                        end = time.time()
                        print(msg.format(
                            i, args.epochs,
                            j, apsp.shape[0],
                            np.mean(losses),
                            end - start
                        ))
                        losses = []
                        start = end
        except (KeyboardInterrupt):
            pass

        print('Saving')

        out = np.zeros((apsp.shape[0], args.dims))
        for j in range(0, apsp.shape[0], args.batch_size):
            batch = apsp[j:j+args.batch_size]
            result = sess.run(compressed, feed_dict={vec_input: batch})
            out[j:j+args.batch_size, :] = result

        np.save(args.outfile, out)
