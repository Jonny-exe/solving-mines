import numpy as np
import random
from main import MinesGame
class Bot():
    def __init__(self, game):
        self.game = game

    def render_games():
        game.render_games()


    def look_for_empty(self):
        index = 0
        self.over = False
        for rowIndex in range(len(self.game.game_board)):
            row = self.game.game_board[rowIndex]
            if self.over:
                break
            for columnIndex in range(len(row)):
                if self.over:
                    break
                index += 1
                column = self.game.game_board[rowIndex][columnIndex]
                if column == 0:
                    #LEFT
                    if columnIndex > 0:
                        #MIDDLE
                        if self.game.game_board[rowIndex][columnIndex - 1] == -2:
                            number = ((rowIndex * self.game.WIDTH) + columnIndex - 1)
                            self.send_input(number)
                            return self.number_to_action(number)

                        #TOP
                        if rowIndex > 0:
                            if self.game.game_board[rowIndex - 1][columnIndex - 1] == -2:
                                number = (((rowIndex - 1)* self.game.WIDTH) + columnIndex - 1)
                                self.send_input(number)
                                return self.number_to_action(number)

                        #BOTTOM
                        if len(self.game.game_board) - 1 > rowIndex:
                            if self.game.game_board[rowIndex + 1][columnIndex - 1] == -2:
                                number = (((rowIndex + 1) * self.game.WIDTH) + columnIndex - 1)
                                self.send_input(number)
                                return self.number_to_action(number)

                    #RIGHT
                    if len(row) - 1 > columnIndex:
                        #MIDDLE
                        if self.game.game_board[rowIndex][columnIndex + 1] == -2:
                            number = ((rowIndex * self.game.WIDTH) + columnIndex + 1)
                            self.send_input(number)
                            return self.number_to_action(number)

                        #TOP
                        if rowIndex > 0:
                            if self.game.game_board[rowIndex - 1][columnIndex + 1] == -2:
                                number = (((rowIndex - 1)* self.game.WIDTH) + columnIndex + 1)
                                self.send_input(number)
                                return self.number_to_action(number)

                        #BOTTOM
                        if len(self.game.game_board) - 1 > rowIndex:
                            if self.game.game_board[rowIndex + 1][columnIndex + 1] == -2:
                                number = (((rowIndex + 1) * self.game.WIDTH) + columnIndex + 1)
                                self.send_input(number)
                                return self.number_to_action(number)

                    #MIDDLE
                    #TOP
                    if rowIndex > 0:
                        if self.game.game_board[rowIndex - 1][columnIndex] == -2:
                            number = (((rowIndex - 1)* self.game.WIDTH) + columnIndex)
                            self.send_input(number)
                            return self.number_to_action(number)

                    #BOTTOM
                    if len(self.game.game_board) - 1 > rowIndex:
                        if self.game.game_board[rowIndex + 1][columnIndex] == -2:
                            number = (((rowIndex + 1)* self.game.WIDTH) + columnIndex)
                            self.send_input(number)
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

    #FIXME Inecessary
    def send_input(self, number):
        if self.over:
            return
        self.over = True
        action = self.number_to_action(number)
        # self.game.enter_input(action)



