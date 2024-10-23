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

    def check(self, n, x, y) -> bool:
        """
        This method is supposed to check whether placing the number n at position (x, y) is valid according to
        Sudoku rules. It would return True if valid, False otherwise
        """

        if n not in self.unique_rows[x] and n not in self.unique_cols[y] and n not in self.unique_areas[y // 3 * 3 + x // 3]:
            return True

        return False

    def remove(self, x, y):
        """
        Removes the number from the board at the specified position (x, y). Additionally, it should update the
        tracking sets (unique_areas, unique_rows, unique_cols).
        """
        n = self.rows[y][x]

        self.rows[y][x] = '0'
        self.unique_cols[y].discard(n)
        self.unique_rows[x].discard(n)
        self.unique_areas[x//3 * 3 + y//3].discard(n)

    def insert(self, n, x, y):
        """
        Inserts the number n at the specified position (x, y) on the board and adds it to the relevant sets
        (for checking rows, columns, and 3x3 grids). It should also return a message indicating success or failure.
        """
        self.rows[y][x] = f'{n}'
        self.unique_cols[y].add(n)
        self.unique_rows[x].add(n)
        self.unique_areas[x//3 * 3 + y//3].add(n)

        return 'success'


    def is_finished(self) -> bool:
        """
        This method should return True if the game is complete (all cells are filled and valid),
        or False if the puzzle is not yet solved.
        """
        for i, row in enumerate(self.rows):
            for j, n in enumerate(row):
                if n == 0 or not self.check(n, j, i):
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
