# -*- encoding:utf-8 -*-
import sys
sys.path.append('../../')

import numpy as np

from lightnn.models.NeuralNetwork import NetWork
from lightnn.base.losses import MeanSquareLoss, BinaryCategoryLoss, LogLikelihoodLoss


def gradient_check(nn, check_layer=0):
    """
    Check the gradient calculated by BP algorithm

    :param check_layer: The layer you want to make gradient check
    :return: None
    """
    random_input = (np.random.random([nn.sizes[0]]) * 2 - 1)
    random_label = np.zeros([nn.sizes[-1]])
    random_label[np.random.randint(0, nn.sizes[-1])] = 1

    a = nn.feedforward(random_input)
    nn.backprop(random_label)
    real_delta = nn.layers[check_layer].delta_W[0, 0]
    w = nn.layers[check_layer].W[0, 0]
    h = 1e-3
    nn.layers[check_layer].W[0, 0] -= h
    a = nn.feedforward(random_input)
    cost1 = nn.cost.forward(a, random_label)
    nn.layers[check_layer].W[0, 0] += 2 * h
    a = nn.feedforward(random_input)
    cost2 = nn.cost.forward(a, random_label)
    check_delta = (cost2 - cost1) / (2 * h)
    print 'Value of W[{},0,0] is {}, real gradient is {}, ' \
          'and check gradient is {}'.format(check_layer, w, real_delta, check_delta)


if __name__ == '__main__':
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets('/tmp/data', one_hot=True)
    training_data = np.array([image.flatten() for image in mnist.train.images])
    training_label = mnist.train.labels
    net = NetWork([728, 300, 10], lmbda=0.1, cost=LogLikelihoodLoss)
    # gradient check
    gradient_check(net, 1)
    # model trained to classify the mnist dataset
    net.train(training_data, training_label, 20, 64)
