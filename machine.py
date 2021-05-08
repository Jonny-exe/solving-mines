import random
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
INITIAL_GAMES = 20000
SCORE_REQUIREMENTS = 4


def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    for _ in range(INITIAL_GAMES):
        game = main.MinesGame(WIDTH, HEIGHT)
        score = 0
        game_memory = []
        for _ in range(GOAL_STEPS):
            action = [
                random.randrange(0, WIDTH),
                random.randrange(0, HEIGHT),
                random.randrange(0, 2),
            ]
            observation, done, reward = game.enter_input(
                action[0], action[1], action[2]
            )

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
    print("Average accpedted score: ", mean(accepted_scores))
    return training_data


def neuronal_network_model(input_size):
    network = input_data(shape=[None, input_size, 8], name="input")

    network = fully_connected(network, 128, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation="relu")
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation="relu")
    network = dropout(network, 0.8)

    # 2 Is probably wrong.
    network = fully_connected(network, 3, activation="softmax")
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
    # x = np.array(training_data).reshape(-1, len(training_data[0][0], 1))
    y = [i[1] for i in training_data]
    print()
    if not model:
        model = neuronal_network_model(input_size=len(x[0]))

    print("FIT")

    model.fit(
        {"input": x},
        {"targets": y},
        n_epoch=3,
        snapshot_step=500,
        show_metric=True,
        run_id="openaistuff",
    )

    return model


training_data = initial_population()
model = train_model(training_data)


scores = []
choices = []
for each_game in range(1):
    score = 0
    game_memory = []
    game = main.MinesGame(8, 8)
    observations = game.get_game_board()

    for _ in range(GOAL_STEPS):
        game.render_games()
        x = np.array(observations).reshape(
            (-1, len(training_data[0][0]), HEIGHT)
        )
        action = model.predict(
            # np.array(observations).reshape(-1, len(observations[0]), HEIGHT)
            x
        )[0]
        action = [round(number) for number in action]
        print("ACTION: ", action)
        choices.append(action)

        observation, done, reward = game.enter_input(action[0], action[1], action[2])
        game_memory.append([observation, action])
        score += reward
        if done:
            break
    scores.append(score)

average = sum(scores) / len(scores)
print("Average score: ", average)

model.save(f"models/A-{average}.model")
