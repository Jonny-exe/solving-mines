import random
import copy
from create_data import initial_population
from datetime import datetime
from beautifultable import BeautifulTable
from time import gmtime, strftime
from bot import Bot
import sys
import math
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from statistics import mean, median
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import numpy as np
import game

LR = 1e-3
HEIGHT = 8
WIDTH = 8
EPOCHS = 5
GOAL_STEPS = 500
# 9 best


def neuronal_network_model(input_size):
    # FIXME: probably don't even need max pooling "https://deeplizard.com/learn/video/ZjM_XQa5s6s"
    # TODO: also see http://tflearn.org/data_augmentation/#image-augmentation for better results
    # TODO: example for CNN https://www.kaggle.com/rhammell/tflearn-convolutional-neural-network
    # TODO: add data_prepocessing and data_augmentation for better results in input_data

    #                                                       3
    network = input_data(shape=[None, input_size, WIDTH, 1], name="input")
    network = conv_2d(network, 32, 3, activation="relu")
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 64, 3, activation="relu")
    network = conv_2d(network, 64, 3, activation="relu")
    network = max_pool_2d(network, 2)
    network = fully_connected(network, 512, activation="relu")
    network = dropout(network, 0.5)
    network = fully_connected(network, WIDTH * HEIGHT, activation="softmax")
    network = regression(
        network, optimizer="adam", loss="categorical_crossentropy", learning_rate=LR
    )

    model = tflearn.DNN(network, tensorboard_dir="log")
    return model


def train_model(training_data, model=False):
    print("train")
    x = np.array([i[0] for i in training_data])
    print(x)
    x = x.reshape((-1, WIDTH, WIDTH, 1))

    y = [i[1] for i in training_data]
    if not model:
        model = neuronal_network_model(input_size=len(x[0]))

    print("FIT")

    model.fit(
        # {"input": x},
        # {"targets": y},
        x,
        y,
        shuffle=True,
        n_epoch=EPOCHS,
        snapshot_step=500,
        show_metric=True,
        run_id="openaistuff",
    )

    date = strftime("%Y-%m-%d-%H:%M:%S")
    model.save(f"models/A-{date}.model")
    return model
