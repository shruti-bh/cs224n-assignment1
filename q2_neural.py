#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(data, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.

    Arguments:
    data -- M x Dx matrix, where each row is a training example.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    ### YOUR CODE HERE: forward propagation
    M = data.shape[0]
    z1 = data.dot(W1) + b1 # M x H
    h1 = sigmoid(z1) # M x H
    z2 = h1.dot(W2) + b2 # M x Dy
    y_pred = softmax(z2) # M x Dy
    cost = - np.sum(np.log(y_pred) * labels) / float(M) 
    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation
    gradz2 = (y_pred - labels) / float(M) # M x Dy
    gradh1 = gradz2.dot(W2.T) # (M x Dy) * (Dy x H) = (M x H)
    gradW2 = h1.T.dot(gradz2)  #  (H x M) * (M x Dy) = (H x Dy)
    gradb2 = np.sum(gradz2, axis=0) # (1 x Dy)
    gradz1 = gradh1 * sigmoid_grad(h1)# (M x H)
    gradW1 = data.T.dot(gradz1) # (Dx x M) * (M x H)
    gradb1 = np.sum(gradz1, axis=0) # (1 x H)
    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    N = 100
    dimensions = [40, 60, 5]
    data = np.random.randn(N, dimensions[0])
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0, dimensions[2]-1)] = 1
    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
                dimensions[1] + 1) * dimensions[2], )
    gradcheck_naive(lambda params:
                    forward_backward_prop(data, labels, params, dimensions), params)
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
