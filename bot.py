import numpy as np
import random
from main import MinesGame
from typing import Union
class Bot():
    def __init__(self, game):
        self.game = game
        self.render_games()

    def render_games(self):
        game.render_games()

    def coordenates_to_number(self, x: int, y: int) -> int:
        number = ((y * self.game.WIDTH) + x)
        print("NUMBER: ", number)
        return number


    def look_for_empty(self):
        index = 0
        self.over = False
        for row_index in range(len(self.game.game_board)):
            row = self.game.game_board[row_index]
            if self.over:
                break
            for column_index in range(len(row)):
                if self.over:
                    break
                index += 1
                column = self.game.game_board[row_index][column_index]
                if column == 0:
                    neighbours_instance = Neighbours([column_index, row_index], game.board)
                    neighbours = neighbours_instance.get_neightbours(column_index, row_index)
                    for neighbour in neighbours:
                        x = neighbour[0]
                        y = neighbour[1]
                        desired_position = neighbour[2]
                        if neighbours_instance.exists(x, y, desired_position):
                            print(f"x: {column_index}, y: {row_index}")
                            print(neighbours)
                            if self.game.game_board[y][x] == -2:
                                print(x, y)
                                number = self.coordenates_to_number(x, y)
                                return self.number_to_action(number)


        action = [0 for _ in range(self.game.WIDTH*self.game.HEIGHT)]
        action[random.randrange(0, self.game.WIDTH*self.game.HEIGHT)] = 1
        return np.array(action)


    def number_to_action(self, number):
        action = []
        for i in range(self.game.WIDTH * self.game.HEIGHT):
            action.append(0)

        action[number] = 1
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
            if y > 0 and x > 0 :
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



game = MinesGame(8, 8)
bot = Bot(game)
game.print_board()
output = np.argmax(bot.look_for_empty())
output = game.get_mine_location_from_int(output)
print(output)
