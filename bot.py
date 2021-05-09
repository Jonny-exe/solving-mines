import numpy as np
from main import MinesGame
class Bot():
    def __init__(self, game):
        self.game = game
        game.render_games()
        self.look_for_empty()

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
                            self.send_input((rowIndex * self.game.WIDTH) + columnIndex - 1)

                        #TOP
                        if rowIndex > 0:
                            if self.game.game_board[rowIndex - 1][columnIndex - 1] == -2:
                                self.send_input(((rowIndex - 1)* self.game.WIDTH) + columnIndex - 1)

                        #BOTTOM
                        if len(self.game.game_board) - 1 > rowIndex:
                            if self.game.game_board[rowIndex + 1][columnIndex - 1] == -2:
                                self.send_input(((rowIndex + 1) * self.game.WIDTH) + columnIndex - 1)

                    #RIGHT
                    if len(row) - 1 > columnIndex:
                        #MIDDLE
                        if self.game.game_board[rowIndex][columnIndex + 1] == -2:
                            self.send_input((rowIndex * self.game.WIDTH) + columnIndex + 1)

                        #TOP
                        if rowIndex > 0:
                            if self.game.game_board[rowIndex - 1][columnIndex + 1] == -2:
                                self.send_input(((rowIndex - 1)* self.game.WIDTH) + columnIndex + 1)

                        #BOTTOM
                        if len(self.game.game_board) - 1 > rowIndex:
                            if self.game.game_board[rowIndex + 1][columnIndex + 1] == -2:
                                self.send_input(((rowIndex + 1) * self.game.WIDTH) + columnIndex + 1)

                    #MIDDLE
                    #TOP
                    if rowIndex > 0:
                        if self.game.game_board[rowIndex - 1][columnIndex] == -2:
                            self.send_input(((rowIndex - 1)* self.game.WIDTH) + columnIndex)

                    if len(self.game.game_board) - 1 > rowIndex:
                        if self.game.game_board[rowIndex + 1][columnIndex] == -2:
                            self.send_input(((rowIndex - 1)* self.game.WIDTH) + columnIndex)






    def number_to_action(self, number):
        action = []
        for i in range(self.game.WIDTH * self.game.HEIGHT):
            action.append(0)

        action[number] = 1
        return np.array(action)

    def send_input(self, number):
        if self.over:
            return
        action = self.number_to_action(number)
        self.game.enter_input(action)
        self.game.print_board()
        self.over = True



game = MinesGame(8, 8)
bot = Bot(game)
