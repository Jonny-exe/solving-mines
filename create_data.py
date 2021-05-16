from game import MinesGame
import numpy as np
from copy import deepcopy
from statistics import mean, median
from bot import Bot

INITIAL_GAMES = 100
SCORE_REQUIREMENTS = 35
HEIGHT = 8
WIDTH = 8
GOAL_STEPS = 500
accepted_scores = []

def initial_population():
    training_data = []
    scores = []
    for i in range(INITIAL_GAMES):
        if i % 1000 == 0:
            print(f"{i} / {INITIAL_GAMES}")

        game = MinesGame(WIDTH, HEIGHT)
        # game.render_games()
        bot = Bot(game)
        score = 0
        game_memory = []
        prev_observation = deepcopy(game.game_board)
        for _ in range(GOAL_STEPS):
            action = bot.look_for_empty()
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
            for data in game_memory:
                training_data.append(data)

        scores.append(score)
    training_data_save = np.array(training_data)
    print("Average accepted score: ", mean(accepted_scores))
    print("Accepted scores: ", len(accepted_scores))
    return training_data

if __name__ == "__main__":
    data = initial_population()
    np.save(f"training_data/G-{INITIAL_GAMES}-A-{mean(accepted_scores)}-acce", data, allow_pickle=True)

