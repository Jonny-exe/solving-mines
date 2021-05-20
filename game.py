import random
from typing import Tuple
import math
import array
from beautifultable import BeautifulTable
import numpy as np


class MinesGame:
    def __init__(self, height, width, human=False):
        self.HEIGHT = height
        self.WIDTH = width
        MINES_RATIO = 0.12
        self.MINES_AMOUNT = int(round((MINES_RATIO * (self.WIDTH * self.HEIGHT)), 0))
        self.mines_location = self.get_mines_location()
        self.create_board()
        self.render = False
        if human:
            print(f"MINES: {self.MINES_AMOUNT}")
            print(f"MINES LOCATION: {self.mines_location}")
            self.print_board()
            self.start_game()

    def start_game(self):
        over = False
        while not over:
            over = self.ask_for_input()

        won = not self.check_if_correct()
        if won:
            print("You won")
        else:
            print("You lost")

    def render_games(self):
        self.render = True

    def enter_input(self, mine_location) -> Tuple[list, bool, int]:
        # mine_location = np.argmax(mine_location)
        row = math.floor(mine_location / self.WIDTH)
        column = (mine_location % self.HEIGHT)
        over = False
        won = False
        reward = 1
        hit_square = self.board[row][column]
        if (hit_square == -1) or (hit_square  == 0) or (self.game_board[row][column] != -2):
            if hit_square == -1:
                self.game_board[row][column] = self.board[row][column]

            over = True
            reward = 0
        else:
            self.game_board[row][column] = self.board[row][column]
            self.locations_free -= 1

        if self.render:
            self.print_board()

        if self.locations_free == 0:
            over = True
            won = True



        return self.game_board, over, reward, won


    def check_if_correct(self):
        # Check if the result is correct
        wrong = False
        mine_count = 0
        for mine_location in self.mines_location:
            mine_location = {
                "row": math.floor(mine_location / self.WIDTH) - 1,
                "column": (mine_location % self.HEIGHT) - 1
            }

            if self.game_board[mine_location["row"]][column_index] != -3:
                wrong = True
                break
            else:
                mine_count += 1

        print(f"MINE_COUNT: {mine_count}")
        return wrong

    def get_mine_location_from_int(self, number):
        mine_location = {
            "row": math.floor(number / self.WIDTH),
            "column": number % self.HEIGHT
        }
        return mine_location

    def create_and_fill_board(self, item_to_fill=0):
        board = []
        for column in range(self.WIDTH):
            board.append([])
            for _row in range(self.HEIGHT):
                board[column].append(item_to_fill)
        return board



    def print_board(self, game=True, board=None):
        symbols_map = {
            "-2": "🟩",
            "0": "🟫",
            "1": "𝟣",
            "2": "𝟤",
            "3": "𝟥",
            "4": "𝟦",
            "5": "𝟧",
            "6": "𝟨",
            "7": "𝟩",
            "8": "𝟪"
        }
        if board is None:
            board = self.game_board

        index = 0
        table = BeautifulTable()
        for row in board:
            fancy_row = []
            for column_index in range(len(row)):
                fancy_row.append(symbols_map[str(row[column_index])])
            table.append_row(fancy_row)
            index += 1

        print(table)


    def create_board(self):
        # FIXME: use the create_and_fill_board function
        self.board = []
        self.game_board = []
        # Fill with 0
        for column in range(self.WIDTH):
            self.board.append([])
            self.game_board.append([])
            for _row in range(self.HEIGHT):
                self.board[column].append(0)
                # -2 is equal to not seen
                self.game_board[column].append(-2)


        # Put in all +1 the ones that touch the mines
        for mine_location in self.mines_location:
            # Transform from the numbers to column and row
            # -1 is becuase it's not 0 indexed
            mine_location = {
                "row": math.floor(mine_location / self.WIDTH),
                "column": (mine_location % self.HEIGHT)
            }
            row_index = mine_location["row"]
            column_index = mine_location["column"]


            # +1 To fields next to it
            # TOP
            if row_index > 0:

                # MIDDLE
                self.board[row_index - 1][column_index] += 1

                # RIGHT
                if column_index < self.WIDTH - 1:
                    self.board[row_index - 1][column_index + 1] += 1

                # LEFT
                if column_index > 0:
                    self.board[row_index - 1][column_index - 1] += 1

            # MIDDLE 


            if column_index > 0:
                self.board[row_index][column_index - 1] += 1

            if column_index < self.WIDTH - 1:
                self.board[row_index][column_index + 1] += 1

            # BOTTOM

            if mine_location["row"] < self.HEIGHT - 1:

                # MIDDLE
                self.board[row_index + 1][column_index] += 1

                # RIGHT
                if column_index < self.WIDTH - 1:
                    self.board[row_index + 1][column_index + 1] += 1

                # LEFT
                if column_index > 0:
                    self.board[row_index + 1][column_index - 1] += 1

        # Write all the mines
        for mine_location in self.mines_location:
            mine_location = {
                "row": math.floor(mine_location / self.WIDTH),
                "column": (mine_location % self.HEIGHT)
            }
            self.board[mine_location["row"]][mine_location["column"]] = -1

        zeros = 0
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
                if self.board[row][column] == 0:
                    self.game_board[row][column] = 0
                    zeros += 1

        self.locations_free = (self.HEIGHT * self.WIDTH) - zeros - self.MINES_AMOUNT


    def get_zeros_in_board(self):
        zeros_in_board = 0
        for row in self.board:
            for square in row:
                if square == 0:
                    zeros_in_board += 1
        return zeros_in_board



    def ask_for_input(self) -> bool:
        row = int(input("ROW: ")) - 1
        column = int(input("COLUMN: ")) - 1
        flag = input("FLAG: ")
        finished = input("HAVE YOU FINISHED: ")
        if finished == "True":
            finished = True
        else:
            finished = False



        print(f"FINISHED: {finished}")
        print(f"GUESSED: {self.board[row][column]}")
        if flag == "True":
            # M is equal to -3
            self.game_board[row][column] = -3
        else:
            self.game_board[row][column] = self.board[row][column]
        self.print_board()
        return finished


    def get_mines_location(self) -> list:
        ocupied_numbers = {}
        random_numbers = []
        for _number in range(self.MINES_AMOUNT):
            random_number = random.randint(0, ((self.HEIGHT * self.WIDTH) - 1))
            if not random_number in ocupied_numbers:
                random_numbers.append(random_number)
                ocupied_numbers[random_number] = "ocupied"

        # I sorted them so I can find them easier when I create the board
        sorted_numbers = sorted(random_numbers)
        return sorted_numbers



