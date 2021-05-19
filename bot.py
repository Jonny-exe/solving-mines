import numpy as np
import sys
from statistics import mean, median
import copy
import random
from game import MinesGame
from typing import Union

class Bot():
    def __init__(self, game):
        self.game = game
        self.mines_board = game.create_and_fill_board(0)
        self.debug = False
        self.over = False
        self.moves = 0



    def render_games(self):
        self.game.render_games()

    def coordenates_to_number(self, x: int, y: int) -> int:
        number = ((y * self.game.WIDTH) + x)
        return number


    def look_for_empty(self):
        #TODO: maybe do this only once for all the mines and then access it
        self.over = False
        # Check if there is some 0 adjecent which is a sure not bomb
        for row_index in range(len(self.game.game_board)):
            row = self.game.game_board[row_index]
            if self.over:
                break
            for column_index in range(len(row)):
                column = self.game.game_board[row_index][column_index]
                if column == 0:
                    neighbours_instance = Neighbours([column_index, row_index], self.game.board)
                    neighbours = neighbours_instance.get_neightbours(column_index, row_index)
                    for neighbour in neighbours:
                        x = neighbour[0]
                        y = neighbour[1]
                        desired_position = neighbour[2]
                        if neighbours_instance.exists(x, y, desired_position):
                            if self.game.game_board[y][x] == -2:
                                number = self.coordenates_to_number(x, y)
                                return self.number_to_action(number)

        # return self.random_action()
        return self.look_for_best(0)

        # action = [0 for _ in range(self.game.WIDTH*self.game.HEIGHT)]
        # action[random.randrange(0, self.game.WIDTH*self.game.HEIGHT)] = 1
        # return np.array(action)



    def mark_mines(self, neighbours, column):
        free_squares = []
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]

            neighbour_value = self.game.game_board[y][x]
            if neighbour_value == -2:
                free_squares.append([x, y])

        if len(free_squares) == column:
            index = 0
            for square_index in range(len(free_squares)):
                square = free_squares[square_index]
                x = square[0]
                y = square[1]
                self.mines_board[y][x] = 1

    def find_free_move(self, neighbours, column, mine_value_index):
        mines_neighbour = 0
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            neighbour_value = self.game.game_board[y][x]
            if self.mines_board[y][x] == 1:
                mines_neighbour += 1

        if mines_neighbour == column:
            for neighbour in neighbours:
                x = neighbour[0]
                y = neighbour[1]
                neighbour_value = self.game.game_board[y][x]
                if neighbour_value == -2 and self.mines_board[y][x] != 1:
                    number = self.coordenates_to_number(x, y)
                    if self.debug:
                        print(f"Return, x: {x}, y:  {y}")
                    return self.number_to_action(number)

        return np.array([])


    def look_for_best(self, mine_value_index) -> Union[bool, list]:
        mine_value_index  = mine_value_index + 1

        if mine_value_index > 5:
            return self.random_action()
        self.over = False

        # Check if there is some 0 adjecent which is a sure not bomb
        for mine_target_value_index in range(5):
            for row_index in range(len(self.game.game_board)):
                row = self.game.game_board[row_index]
                if self.over:
                    break
                for column_index in range(len(row)):
                    if self.over:
                        break
                    column = self.game.game_board[row_index][column_index]
                    if column == mine_target_value_index:
                        neighbours_instance = Neighbours([column_index, row_index], self.game.board)
                        neighbours = neighbours_instance.get_neightbours(column_index, row_index)
                        neighbours = neighbours_instance.remove_non_existing_neighbours([column_index, row_index], neighbours,
                                                    neighbours_instance)
                        self.mark_mines(neighbours, column)

        for row_index in range(len(self.game.game_board)):
            row = self.game.game_board[row_index]
            if self.over:
                break
            for column_index in range(len(row)):
                if self.over:
                    break
                column = self.game.game_board[row_index][column_index]
                if column == mine_value_index:
                    # print("square equal to mine_value_index")
                    neighbours_instance = Neighbours([column_index, row_index], self.game.board)
                    neighbours = neighbours_instance.get_neightbours(column_index, row_index)
                    neighbours = neighbours_instance.remove_non_existing_neighbours([column_index, row_index], neighbours,
                                                neighbours_instance)
                    # self.mark_mines(neighbours, column)
                    result = self.find_free_move(neighbours, column, mine_value_index)
                    if result.size != 0:
                        self.moves += 1
                        return result

        return self.look_for_best(mine_value_index + 1)



    def number_to_action(self, number):
        action = [0 for _ in range(self.game.WIDTH*self.game.HEIGHT)]
        action[number] = 1
        return np.array(action)

    def random_action(self):
        random_number = random.randrange(0, self.game.WIDTH*self.game.HEIGHT)
        return self.number_to_action(random_number) 

    def random_secure_action(self):
        if self.over:
            return
        index = 0
        for row_index in range(self.game.WIDTH):
            for column_index in range(self.game.WIDTH):
                square = self.game.game_board[row_index][column_index]
                if square == -2:
                    return self.number_to_action(index)
                index += 1


class Neighbours():
    def __init__(self, square_position: list, board, desired_position=""):
        self.board = board
        self.WIDTH = len(board)
        self.desired_position = desired_position
        self.x = square_position[0]
        self.y = square_position[1]
        self.value = self.get_value(self.x, self.y)


    def get_value(self, x, y) -> Union[bool, int]:
        value = -1
        exists = False
        desired_position = self.desired_position
        if desired_position == "top" and self.exists(x, y, desired_position):
                value = self.board[x][y + 1]
                exists = True
        if desired_position == "topright" and self.exists(x, y, desired_position):
                value = self.board[y - 1][x + 1]
                exists = True

        if desired_position == "topleft" and self.exists(x, y, desired_position):
                value = self.board[y - 1][x - 1]
                exists = True

        if desired_position == "right" and self.exists(x, y, desired_position):
                value = self.board[y][x + 1]
                exists = True

        if desired_position == "left" and self.exists(x, y, desired_position):
                value = self.board[y][x - 1]
                exists = True

        if desired_position == "bottom" and self.exists(x, y, desired_position):
                value = self.board[y + 1][x]
                exists = True

        if desired_position == "bottomright" and self.exists(x, y, desired_position):
                value = self.board[y + 1][x + 1]
                exists = True

        if desired_position == "bottomleft" and self.exists(x, y, desired_position):
                value = self.board[y + 1][x - 1]
                exists = True

        if not exists:
            return exists
        else:
            return value

    def get_neightbours(sefl, x, y):
        neighbours = []
        neighbours.append([x + 1, y, "right"])
        neighbours.append([x + 1, y + 1, "bottomright"])
        neighbours.append([x + 1, y - 1, "topright"])
        neighbours.append([x - 1, y, "left"])
        neighbours.append([x - 1, y + 1, "bottomleft"])
        neighbours.append([x - 1, y - 1, "topleft"])
        neighbours.append([x, y - 1, "top"])
        neighbours.append([x, y + 1, "bottom"])
        return neighbours


    def exists(self, x, y, desired_position) -> Union[bool, int]:
        exists = False
        if desired_position == "top":
            if y > 0:
                exists = True

        if desired_position == "topright":
            if y > 0 and x < self.WIDTH - 1:
                exists = True

        if desired_position == "topleft":
            if y > 0 and x > 0:
                exists = True
        if desired_position == "right":
            if x < self.WIDTH - 1:
                exists = True

        if desired_position == "left":
            if x > 0:
                exists = True

        if desired_position == "bottom":
            if y < self.WIDTH - 1:
                exists = True

        if desired_position == "bottomright":
            if y < self.WIDTH - 1 and x < self.WIDTH - 1:
                exists = True

        if desired_position == "bottomleft":
            if y < self.WIDTH - 1 and x > 0:
                exists = True

        return exists



    def remove_non_existing_neighbours(self, position, neighbours, neighbours_instance):
        neighbours = copy.deepcopy(neighbours)
        index = 0
        x = position[0]
        y = position[1]
        # for neighbour_index in range(len(neighbours)):
        while index < len(neighbours):
            neighbour = neighbours[index]
            desired_position = neighbour[2]

            if not neighbours_instance.exists(x, y, desired_position):
                neighbours.pop(index)
            else:
                index += 1
        return neighbours




def test(amount):
    tries = 50
    games = 100 if amount != "single" else 1
    scores = []
    wins = []
    debug = True

    for _ in range(games):
        game = MinesGame(8, 8)
        bot = Bot(game)
        if debug:
            bot.debug = True
            game.print_board()
        for i in range(tries):
            action = bot.look_for_empty()

            if debug:
                print(i)
                print("action: ", action)
            observation, done, reward, won = game.enter_input(action)
            if done:
                if debug:
                    game.print_board(board=bot.mines_board)
                    game.print_board()
                    print("Moves; ", bot.moves)
                    print("WON: ", won)
                scores.append(i)
                if won:
                    wins.append(1)
                else:
                    wins.append(0)
                break
    print(scores)
    print("Average score: ", mean(scores))
    print("Average win: ", mean(wins))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test(sys.argv[2])

