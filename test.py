#!/usr/bin/python
from game import MinesGame
from time import strftime
from net import Net
import torch
import numpy as np

WIDTH = 8
GOAL_STEPS = 500
scores = []
choices = []
wins = []
print_rounds = False


def test(net, show_games):
    print("START")
    date = strftime("%Y-%m-%d-%H:%M:%S")
    print(date)
    for each_game in range(100):
        game_memory = []
        game = MinesGame(8, 8)
        observations = game.game_board
        score = 0
        for _ in range(GOAL_STEPS):
            board = observations
            board = torch.Tensor(board)
            board = board.reshape([1, 1, 8, 8])

            action = net(board)
            prediction = torch.max(action, 1)

            if show_games:
                print(action)
            action = torch.max(action).item()
            action = prediction[1].item()
            # action = int(round(action, 0))
            if show_games:
                game.print_board()

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


if __name__ == "__main__":
    net = Net()
    net.load_state_dict(torch.load("models/value.pth"))

    import argparse

    parser = argparse.ArgumentParser(description="Main file")
    parser.add_argument("--print", type=bool)

    args = parser.parse_args()

    if args.print:
        show_games = True
    elif args.print is None:
        show_games = False

    test(net, show_games)
