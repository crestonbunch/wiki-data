import argparse
import numpy as np
import tensorflow as tf
import time
from math import ceil


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate a lower dimensional matrix using vector emebeddings')
    parser.add_argument('--infile', default='apsp.npy',
                        help='APSP matrix')
    parser.add_argument('--outfile', default='embeddings.npy',
                        help='Embeddings output matrix')
    parser.add_argument('--dims', default=100, type=int,
                        help='Number of dimensions in the vector embeddings')
    parser.add_argument('--batch_size', default=1000, type=int,
                        help='Number of nodes to process each iteration')
    parser.add_argument('--epochs', default=1, type=int,
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

    embeddings = tf.Variable(tf.random_normal((apsp.shape[0], args.dims)))

    dataset = tf.data.Dataset.from_generator(
        lambda: gen_inputs(apsp),
        (tf.int32, tf.int32, tf.int32),
        (tf.TensorShape([]), tf.TensorShape([]), tf.TensorShape([]))
    ). \
        shuffle(buffer_size=10*apsp.shape[0]). \
        repeat(args.epochs). \
        batch(args.batch_size)

    iterator = dataset.make_one_shot_iterator()
    input_a, input_b, label = iterator.get_next()
    one_hot_labels = tf.one_hot(label, num_labels)
    embedded_a = tf.nn.embedding_lookup(embeddings, input_a)
    embedded_b = tf.nn.embedding_lookup(embeddings, input_b)
    embedded_a_b = tf.concat((embedded_a, embedded_b), 1)
    dense = tf.layers.dense(embedded_a_b, num_labels,
                            activation=tf.nn.sigmoid)
    loss = tf.losses.softmax_cross_entropy(one_hot_labels, dense)

    global_step = tf.Variable(0, name='global_step', trainable=False)
    learning_rate = 0.01
    train_step = tf.contrib.layers.optimize_loss(
        loss,
        global_step,
        learning_rate,
        'SGD',
        summaries=[]
    )
    init_op = tf.global_variables_initializer()

    total_steps = ceil(num_inputs(apsp) / args.batch_size) * args.epochs
    with tf.Session() as sess:
        sess.run(init_op)

        losses = []
        start = time.time()
        while True:
            try:
                err, i, _ = sess.run([loss, global_step, train_step])
                losses.append(err)
                if i % 1000 == 0:
                    end = time.time()
                    print('Step: {}/{}, Avg loss {:.3f} in {:.3f}s'.format(
                        i, total_steps, np.mean(losses), end - start
                    ))
                    losses = []
                    start = end
            except (tf.errors.OutOfRangeError, KeyboardInterrupt):
                break

        print('Saving')
        out = embeddings.eval()
        np.save(args.outfile, out)
