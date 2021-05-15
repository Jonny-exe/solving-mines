import random
import copy
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
import main

LR = 1e-3
HEIGHT = 8
WIDTH = 8
GOAL_STEPS = 500
INITIAL_GAMES = 40000
SCORE_REQUIREMENTS = 35
EPOCHS = 7
# 9 best



def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    for i in range(INITIAL_GAMES):
        if i % 1000 == 0:
            print(f"{i} / {INITIAL_GAMES}")

        game = main.MinesGame(WIDTH, HEIGHT)
        # game.render_games()
        bot = Bot(game)
        score = 0
        game_memory = []
        prev_observation = copy.deepcopy(game.game_board)
        for _ in range(GOAL_STEPS):
            action = bot.look_for_empty()
            observation, done, reward, won = game.enter_input(action)

            if done:
                break

            data = [prev_observation, action]
            game_memory.append(data)
            prev_observation = copy.deepcopy(observation)

            score += reward

        # if score >= SCORE_REQUIREMENTS:
        if won:
            accepted_scores.append(score)
            for data in game_memory:
                training_data.append(data)

        scores.append(score)
    training_data_save = np.array(training_data)
    print("Average accepted score: ", mean(accepted_scores))
    print("Accepted scores: ", len(accepted_scores))
    # np.save(f"training_data/G-{INITIAL_GAMES}-A-{mean(accepted_scores)}-acce.npy", training_data_save, allow_pickle=True)
    return training_data


def neuronal_network_model(input_size):
    #FIXME: probably don't even need max pooling "https://deeplizard.com/learn/video/ZjM_XQa5s6s"
    #TODO: also see http://tflearn.org/data_augmentation/#image-augmentation for better results
    #TODO: example for CNN https://www.kaggle.com/rhammell/tflearn-convolutional-neural-network
    #TODO: add data_prepocessing and data_augmentation for better results in input_data

    #                                                       3
    network = input_data(shape=[None, input_size, WIDTH, 1], name="input")
    network = conv_2d(network, 32, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 64, 3, activation='relu')
    network = conv_2d(network, 64, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.5)
    network = fully_connected(network, WIDTH*HEIGHT, activation='softmax')
    network = regression(network,
                         optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=LR)

    # model = tflearn.DNN(network, tensorboard_verbose=0)
    model = tflearn.DNN(network, tensorboard_dir="log")
    return model


def train_model(training_data, model=False):
    print("train")
    x = np.array([i[0] for i in training_data])    # x = [i[0] for i in training_data]
    x = x.reshape(
        (-1, WIDTH, WIDTH, 1)
    )

    y = [i[1] for i in training_data]
    if not model:
        model = neuronal_network_model(input_size=len(x[0]))

    print("FIT")

    model.fit(
        # {"input": x},
        # {"targets": y},
        x, y,
        n_epoch=EPOCHS,
        snapshot_step=500,
        show_metric=True,
        run_id="openaistuff",
    )

    return model


if len(sys.argv) > 2:
    if sys.argv[1] == "model":
        new_model = neuronal_network_model(WIDTH)
        new_model.load(sys.argv[2])
        model = new_model
    else:
        print(sys.argv[2])
        training_data = np.load(sys.argv[2], allow_pickle=True)
        model = train_model(training_data)
else:
    training_data = initial_population()
    model = train_model(training_data)


scores = []
choices = []
wins = []
print_rounds = False
for each_game in range(100):
    score = 0
    game_memory = []
    game = main.MinesGame(8, 8)
    observations = game.game_board

    for _ in range(GOAL_STEPS):
        if print_rounds:
            game.render_games()
        x = np.array(observations).reshape((-1,WIDTH, WIDTH, 1))
        action = model.predict(x)[0]

        # x = x.reshape(
            # (-1, WIDTH, WIDTH, 1)
        # )

        mine_location = game.get_mine_location_from_int(np.argmax(action))
        if print_rounds:
            print("ACTION: ", mine_location)

        choices.append(action)

        observations, done, reward, won = game.enter_input(action)
        game_memory.append([observations, action])
        score += reward
        if done:
            break

    print(f"------------------ won: {won} score: {score} -----------------")
    scores.append(score)
    if won:
        wins.append(1)
    else:
        wins.append(0)

average_score = sum(scores) / len(scores)
average_win = sum(wins) / len(scores)
print("Average score: ", average_score)
print("Average win: ", average_win)
date = strftime("%Y-%m-%d-%H:%M:%S")
print(date)

model.save(f"models/A-{average_score}-{date}.model")

