class Board:
    """
    Tic Tac Toe board class.
    """

    def __init__(self):
        """
        Initializes the board with an empty 3x3 grid.
        """
        self.grid = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]

    def place_symbol(self, symbol, x, y):
        """
        Places a symbol at the specified (x, y) coordinates on the board.

        Parameters
        ----------
        symbol : str
            The symbol to place on the board.
        x : int
            The x-coordinate (column) where the symbol should be placed.
        y : int
            The y-coordinate (row) where the symbol should be placed.

        Returns
        -------
        bool
            True if the symbol was successfully placed, False otherwise.
        """
        if x > 2 or x < 0 or y > 2 or y < 0:
            return False
        if self.grid[y][x] != " ":
            return False
        self.grid[y][x] = symbol
        return True

    def get_empty_spots(self):
        """
        Returns a list of tuples representing the coordinates of empty spots on the board.

        Returns
        -------
        list
            A list of tuples (x, y) representing the coordinates of empty spots.
        """
        places = []
        for r in range(len(self.grid)):
            for c in range(3):
                if self.grid[r][c] == " ":
                    places.append((c, r))
        return places

    def is_winner(self, symbol):
        """
        Checks if the specified symbol has won the game.

        Parameters
        ----------
        symbol : str
            The symbol to check for a winning condition.

        Returns
        -------
        bool
            True if the symbol has won, False otherwise.
        """
        winner = False
        for row in range(0, 3):
            if self.grid[row][0] == self.grid[row][1] == self.grid[row][2] == symbol:
                winner = True
        for col in range(0, 3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] == symbol:
                winner = True
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == symbol:
            winner = True
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == symbol:
            winner = True
        return winner

    def is_full(self):
        """
        Checks if the board is full (i.e., no empty spots left).

        Returns
        -------
        bool
            True if the board is full, False otherwise.
        """
        return " " not in (set([rowcol for row in self.grid for rowcol in row]))

    def print(self):
        """
        Prints the current state of the board.
        """
        rows = len(self.grid)
        print("---+---+---")
        for r in range(rows):
            print(self.grid[r][0], " |", self.grid[r][1], "|", self.grid[r][2])
            print("---+---+---")
