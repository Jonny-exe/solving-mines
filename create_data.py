#!/usr/bin/python
from game import MinesGame
import numpy as np
from copy import deepcopy
from statistics import mean, median
from bot import Bot

INITIAL_GAMES = 10000
SCORE_REQUIREMENTS = 35
HEIGHT = 8
WIDTH = 8
GOAL_STEPS = 500
accepted_scores = []


def initial_population():
    # training_data = []
    X = []
    Y = []
    scores = []
    data_count = 0
    while data_count != INITIAL_GAMES:
        if data_count % 1000 == 0:
            print(f"{data_count + 1} / {INITIAL_GAMES}")

        game = MinesGame(WIDTH, HEIGHT)
        # game.render_games()
        bot = Bot(game)
        score = 0
        game_memory = []
        prev_observation = deepcopy(game.game_board)
        for _ in range(GOAL_STEPS):
            action = np.argmax(bot.look_for_empty())
            observation, done, reward, won = game.enter_input(action)

            if done and not won:
                break

            data = [prev_observation, action]
            game_memory.append(data)
            prev_observation = deepcopy(observation)

            score += reward

            if done:
                break
        if won:
            accepted_scores.append(score)
            data_count += 1
            for data in game_memory:
                # training_data.append(data)
                X.append(data[0])
                Y.append(data[1])

        scores.append(score)
    # training_data_save = np.array(training_data)
    print("Average accepted score: ", mean(accepted_scores))
    print("Accepted scores: ", len(accepted_scores))
    return X, Y


if __name__ == "__main__":
    X, Y = initial_population()
    np.savez(f"training_data/data.npz", X, Y, allow_pickle=True)
