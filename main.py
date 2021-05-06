import random
import math
import array


class MinesGame:
    def __init__(self, height, width):
        self.HEIGHT = height
        self.WIDTH = width
        MINES_RATIO = 0.12
        self.MINES_AMOUNT = int(round((MINES_RATIO * (self.WIDTH * self.HEIGHT)), 0))
        print(f"MINES: {self.MINES_AMOUNT}")
        self.board = []
        self.mines_location = self.get_mines_location()
        print(f"MINES LOCATION: {self.mines_location}")
        self.create_board()
        self.print_board()
    
    def start_game(self):
        over = False
        while not over:
            over = self.ask_for_input()
        
        self.check_if_correct()
        
    def check_if_correct(self):
        # Check if the result is correct
        
        return


        

    
    def print_board(self):
        for row in range(self.WIDTH):
            print(self.board[row])


    def create_board(self):
        # Fill with 0
        for column in range(self.WIDTH):
            self.board.append([])
            for _row in range(self.HEIGHT):
                self.board[column].append(0)

        # Put in all +1 the ones that touch the mines
        for mine_location in self.mines_location:
            # Transform from the numbers to column and row
            # -1 is becuase it's not 0 indexed
            mine_location = {
                "row": math.floor(mine_location / self.WIDTH) - 1,
                "column": (mine_location % self.HEIGHT) - 1
            }

            # +1 To fields next to it
            # TOP
            if mine_location["row"] > 0:
                row = self.board[mine_location["row"] - 1]

                # MIDDLE
                row[mine_location["column"]] += 1

                # RIGHT
                if mine_location["column"] + 1 < len(row):
                    row[mine_location["column"] + 1] += 1

                # LEFT
                if mine_location["column"] <= len(row) and mine_location["column"] > 0:
                    row[mine_location["column"] - 1] += 1
            
            # MIDDLE 

            row = self.board[mine_location["row"]]

            if mine_location["column"] > 0:
                row[mine_location["column"] - 1] += 1
            
            if mine_location["column"] < self.WIDTH - 1:
                row[mine_location["column"] + 1] += 1
            
            # BOTTOM

            if mine_location["row"] < self.HEIGHT - 1:
                row = self.board[mine_location["row"] + 1]

                # MIDDLE
                row[mine_location["column"]] += 1

                # RIGHT
                if mine_location["column"] + 1 < len(row):
                    row[mine_location["column"] + 1] += 1

                # LEFT
                if mine_location["column"] <= len(row) and mine_location["column"] > 0:
                    row[mine_location["column"] - 1] += 1

            # Write all the mines
            for mine_location in self.mines_location:
                mine_location = {
                    "row": math.floor(mine_location / self.WIDTH) - 1,
                    "column": (mine_location % self.HEIGHT) - 1
                }
                self.board[mine_location["row"]][mine_location["column"]] = -1
                



    def ask_for_input(self) -> bool:
        column = int(input("COLUMN: "))
        row = int(input("ROW: "))
        finished = bool(input("HAVE YOU FINISHED: "))

        self.board[column][row] = "M"
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


game = MinesGame(8, 8)