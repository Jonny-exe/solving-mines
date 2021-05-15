import numpy as np
import sys
import copy
import random
from main import MinesGame
from typing import Union

class Bot():
    def __init__(self, game):
        self.game = game
        self.mines_board = game.create_and_fill_board(0)
        self.debug = False
        self.over = False



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


    def test(self):
        tries = 30
        for i in range(tries):
            print(i)
            action = self.look_for_empty()
            observation, done, reward = game.enter_input(action)
            if done:
                game.print_board(board=self.mines_board)
                game.print_board()
                break




    def look_for_best(self, mine_value_index) -> Union[bool, list]:
        mine_value_index  = mine_value_index + 1

        if mine_value_index > 5:
            return self.random_action()
        self.over = False

        # Check if there is some 0 adjecent which is a sure not bomb
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
                    free_squares = []
                    for neighbour in neighbours:
                        x = neighbour[0]
                        y = neighbour[1]

                        neighbour_value = self.game.game_board[y][x]
                        # FIXME: maybe you have to take into acount if y and x in mines_board == 1
                        if neighbour_value == -2:
                            free_squares.append([x, y])

                    if len(free_squares) == column:
                        index = 0
                        for square_index in range(len(free_squares)):
                            square = free_squares[square_index]
                            x = square[0]
                            y = square[1]
                            self.mines_board[y][x] = 1
                            # neighbours.pop()

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
                                print("DEBUG: ", self.debug)
                                if self.debug:
                                    print(f"Return, x: {x}, y:  {y}")
                                return self.number_to_action(number)

        return self.look_for_best(mine_value_index + 1)

    def number_to_action(self, number):
        action = []
        for i in range(self.game.WIDTH * self.game.HEIGHT):
            action.append(0)

        action[number] = 1
        return np.array(action)

    def random_action(self):
        action = [0 for _ in range(self.game.WIDTH*self.game.HEIGHT)]
        random_number = random.randrange(0, self.game.WIDTH*self.game.HEIGHT)
        action[random_number] = 1

        return np.array(action)


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



if __name__ == "__main__":
    game = MinesGame(8, 8)
    game.debug = True
    bot = Bot(game)
    game.print_board()
    output = np.argmax(bot.look_for_empty())
    output = game.get_mine_location_from_int(output)

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("ZEROS: ", game.get_zeros_in_board())
        bot.debug = True
        bot.test()
