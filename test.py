from game import MinesGame
import numpy as np
WIDTH = 8
GOAL_STEPS = 500
scores = []
choices = []
wins = []
print_rounds = False

def test():
    for each_game in range(100):
        score = 0
        game_memory = []
        game = MinesGame(8, 8)
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


