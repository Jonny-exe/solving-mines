import random
from datetime import datetime
import sys
import math
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
import numpy as np
import main

LR = 1e-3
HEIGHT = 8
WIDTH = 8
GOAL_STEPS = 500
INITIAL_GAMES = 100000
SCORE_REQUIREMENTS = 5
EPOCHS = 15
# 10 > 3


def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    for _ in range(INITIAL_GAMES):
        game = main.MinesGame(WIDTH, HEIGHT)
        score = 0
        game_memory = []
        for _ in range(GOAL_STEPS):
            action = [0 for _ in range(WIDTH*HEIGHT)]
            action[random.randrange(0, WIDTH*HEIGHT)] = 1
            action = np.array(action)
            observation, done, reward = game.enter_input(action)

            game_memory.append([observation, action])

            score += reward

            if done:
                break
        if score >= SCORE_REQUIREMENTS:
            accepted_scores.append(score)
            for data in game_memory:
                training_data.append(data)

        scores.append(score)
    training_data_save = np.array(training_data)
    # np.save("training_data/saved.npy", training_data_save)
    print("Average accepted score: ", mean(accepted_scores))
    print("Accepted scores: ", len(accepted_scores))
    return training_data


def neuronal_network_model(input_size):
    network = input_data(shape=[None, input_size, 8], name="input")

    network = fully_connected(network, 128, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 1024, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation="relu")
    network = dropout(network, 0.8)

    # 2 Is probably wrong.
    network = fully_connected(network, WIDTH*HEIGHT, activation="softmax")
    network = regression(
        network,
        optimizer="adam",
        learning_rate=LR,
        loss="categorical_crossentropy",
        name="targets",
    )

    model = tflearn.DNN(network, tensorboard_dir="log")
    return model


def train_model(training_data, model=False):
    x = np.array([i[0] for i in training_data]).reshape(
        (-1, len(training_data[0][0]), HEIGHT)
    )
    y = [i[1] for i in training_data]
    if not model:
        model = neuronal_network_model(input_size=len(x[0]))

    print("FIT")

    model.fit(
        {"input": x},
        {"targets": y},
        n_epoch=EPOCHS,
        snapshot_step=500,
        show_metric=True,
        run_id="openaistuff",
    )

    return model


if len(sys.argv) > 1:
    new_model = neuronal_network_model(WIDTH)
    new_model.load(f"models/{sys.argv[1]}")
    model = new_model
    print(type(model))
else:
    training_data = initial_population()
    model = train_model(training_data)


scores = []
choices = []
for each_game in range(10):
    score = 0
    game_memory = []
    game = main.MinesGame(8, 8)
    observations = game.get_game_board()

    for _ in range(GOAL_STEPS):
        game.render_games()
        x = np.array(observations).reshape((-1, WIDTH, HEIGHT))
        action = model.predict(
            # np.array(observations).reshape(-1, len(observations[0]), HEIGHT)
            x
        )[0]
        mine_location = {
            "row": math.floor(np.argmax(action) / WIDTH),
            "column": np.argmax(action) % HEIGHT
        }
        print("ACTION: ", mine_location)

        choices.append(action)

        observations, done, reward = game.enter_input(action)
        game_memory.append([observations, action])
        score += reward
        if done:
            break

    print("-------------------------------------------------------------------")
    scores.append(score)

average = sum(scores) / len(scores)
print("Average score: ", average)

model.save(f"models/A-{average}-{datetime.now()}.model")
