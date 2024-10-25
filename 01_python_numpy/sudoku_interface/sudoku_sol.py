import os
from time import sleep  # Pauses the execution (used to slow down the loop for better user experience).
from utils import _Getch, bcolors, update_position


class Sudoku:
    def __init__(self, path):
        with open(path) as f:
            self.rows = [[int(num.replace('\n', '')) \
                          for num in line.split(",")] for line in f]
        self.initial_values_pos = set()  # set of positions (row, column) where the initial numbers (non-zero) are placed.
        # These numbers cannot be changed by the player.
        self.unique_areas = [set() for _ in range(9)]  # These are sets that will track unique numbers placed in each
        # 3x3 subgrid (area), row, and column, respectively. Each set ensures that the Sudoku rules are maintained
        # (no repeated numbers).
        self.unique_rows = [set() for _ in range(9)]
        self.unique_cols = [set() for _ in range(9)]

        for j, row in enumerate(self.rows):
            for i, num in enumerate(row):
                if num != 0:
                    self.initial_values_pos.add((j, i))
                    self.insert(num, i, j)

    def check(self, n, x, y):
        """
        This method is supposed to check whether placing the number n at position (x, y) is valid according to
        Sudoku rules. It would return True if valid, False otherwise
        """
        # Check if n is already in the row, column, or 3x3 area
        if n in self.unique_rows[y] or n in self.unique_cols[x] or n in self.unique_areas[(y // 3) * 3 + x // 3]:
            return False  # Not allowed
        return True

    def remove(self, x, y):
        """
        Removes the number from the board at the specified position (x, y). Additionally, it should update the
        tracking sets (unique_areas, unique_rows, unique_cols).
        """
        num = self.rows[y][x]
        if num != 0:
            self.rows[y][x] = 0
            self.unique_rows[y].discard(num)
            self.unique_cols[x].discard(num)
            self.unique_areas[(y // 3) * 3 + x // 3].discard(num)

    def insert(self, n, x, y):
        """
        Inserts the number n at the specified position (x, y) on the board and adds it to the relevant sets
        (for checking rows, columns, and 3x3 grids). It should also return a message indicating success or failure.
        """
        # Insert the number if the position is empty and return a message
        if self.rows[y][x] == 0:
            self.rows[y][x] = n
            self.unique_rows[y].add(n)
            self.unique_cols[x].add(n)
            self.unique_areas[(y // 3) * 3 + x // 3].add(n)
            return bcolors.OKGREEN + "Inserted successfully!" + bcolors.ENDC
        return bcolors.WARNING + "Cannot insert here!" + bcolors.ENDC

    def is_finished(self):
        """
        This method should return True if the game is complete (all cells are filled and valid),
        or False if the puzzle is not yet solved.
        """
        for row in self.rows:
            if 0 in row:
                return False
        return True

    def print_highlight(self, x, y, message=""):
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines
        string = " " * width * max((height - 9) // 2, 0)
        for j, row in enumerate(self.rows):
            char_count = max((width - 9) // 3, 0)
            string += " " * max((width - 9) // 3, 0)
            for i, num in enumerate(row):
                if (j, i) in self.initial_values_pos:
                    if x == i and j == y:
                        string += bcolors.BOLD + bcolors.UNDERLINE
                    string += bcolors.RED + str(num) + bcolors.ENDC + " "
                elif x == i and j == y:
                    string += bcolors.UNDERLINE
                    string += bcolors.BOLD + bcolors.OKGREEN + str(num) + bcolors.ENDC + " "
                else:
                    string += str(num) + " "
                char_count += 2
            string += " " * (width - char_count)
        string += " " * width
        char_count = max((width - 9) // 3, 0)
        string += " " * max((width - 9) // 3, 0)
        string += message + " " * (width - len(message) - char_count)
        string += " " * width * max((height - 9) // 2 - 2, 0)
        print(string)


if __name__ == "__main__":
    sudoku = Sudoku("board.csv")
    pos = [0, 0]
    user_input = _Getch()
    message = ""
    while True:
        sudoku.print_highlight(*pos[::-1], message)
        sleep(0.1)
        inp = user_input()
        message = ""
        if inp in {"q", "Q"}:  # Optionally exit with 'q' key
            print(bcolors.WARNING + "Exiting the game..." + bcolors.ENDC)
            break
        if len(inp):
            if not update_position(inp, pos):
                try:
                    num = int(inp)
                    if 1 <= num <= 9:  # Ensure it's a valid Sudoku number
                        # Only remove if the position is not one of the initial values
                        if (pos[0], pos[1]) not in sudoku.initial_values_pos:
                            if sudoku.check(num, pos[1], pos[0]):
                                sudoku.remove(pos[1], pos[0])
                                message = sudoku.insert(num, pos[1], pos[0])
                            else:
                                message = bcolors.RED + "Number is not valid" + bcolors.ENDC
                        else:
                            message = bcolors.WARNING + "Cannot change initial value!" + bcolors.ENDC
                    else:
                        message = bcolors.RED + "Invalid number, use 1-9" + bcolors.ENDC
                except ValueError:
                    message = bcolors.RED + "Input is not a valid number" + bcolors.ENDC

        if sudoku.is_finished():
            print("YOU WON!")
            break
