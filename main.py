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
        self.mines_location = self.get_mines_location()
        print(f"MINES LOCATION: {self.mines_location}")
        self.create_board()
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


        
    def check_if_correct(self):
        # Check if the result is correct
        wrong = False
        mine_count = 0
        for mine_location in self.mines_location:
            mine_location = {
                "row": math.floor(mine_location / self.WIDTH) - 1,
                "column": (mine_location % self.HEIGHT) - 1
            }

            if self.game_board[mine_location["row"]][mine_location["column"]] != "M":
                wrong = True
                break
            else:
                mine_count += 1

        print(f"MINE_COUNT: {mine_count}")
        return wrong


        

    
    def print_board(self, game=True):
        if game:
            board = self.game_board
        else:
            board = self.board
        for row in range(self.WIDTH):
            print(board[row])


    def create_board(self):
        self.board = []
        self.game_board = []
        # Fill with 0
        for column in range(self.WIDTH):
            self.board.append([])
            self.game_board.append([])
            for _row in range(self.HEIGHT):
                self.board[column].append(0)
                self.game_board[column].append("")


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
                if mine_location["column"] + 1 < self.WIDTH:
                    row[mine_location["column"] + 1] += 1

                # LEFT
                if mine_location["column"] <= self.WIDTH - 1 and mine_location["column"] > 0:
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
                if mine_location["column"] < self.WIDTH - 1:
                    row[mine_location["column"] + 1] += 1

                # LEFT
                if mine_location["column"] > 0:
                    row[mine_location["column"] - 1] += 1

            # Write all the mines
            for mine_location in self.mines_location:
                mine_location = {
                    "row": math.floor(mine_location / self.WIDTH) - 1,
                    "column": (mine_location % self.HEIGHT) - 1
                }
                self.board[mine_location["row"]][mine_location["column"]] = -1
            
                
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == 0:
                    self.game_board[row][column] = 0
        self.print_board(False)
        


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
            self.game_board[row][column] = "M"
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


game = MinesGame(8, 8)