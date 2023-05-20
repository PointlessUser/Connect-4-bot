from random import shuffle
from typing import List, Tuple


class Connect4Game:
    def __init__(self, player1: str = "", player2: str = "", in_a_row: int = 4):
        # build the board
        self.in_a_row = in_a_row  # Number of pieces in a row to win
        self.x = in_a_row * 2 - 1  # Width of the board
        self.y = in_a_row + 2 - 1  # Height of the board
        # 2D array representing the board. 0 is empty, 1 is player 1, 2 is player 2
        self.board = [[0 for _ in range(self.x)] for _ in range(self.y)]

        # initialize players
        self.player1 = player1  # JID of player 1
        self.player2 = player2  # JID of player 2
        self.jid_username_map = {}  # Map of JID to username
        self.turn = 1  # 1 or 2 representing which player's turn it is (initialized with player 1 to keep color order consistent)
        self.winner = None  # JID of the winner
        self.game_running = False  # Whether the game is running or not

    def addPlayer(self, player: str, username: str) -> int:
        """
        Adds a player to the game

        :param player: JID of the player to add (str)
        :param username: Username of the player to add (str)

        :return:
        0 if the player was added successfully
        1 if the player is already in the game
        2 if the game is already full
        100 if game is starting after adding the player
        """
        # Check if the player is already in the game
        if player in (self.player1, self.player2):
            return 1

        # Check if the game is already full
        if len(self.jid_username_map) == 2:
            return 2

        # Add the player to the game
        else:
            if self.player1 == "":
                self.player1 = player
            else:
                self.player2 = player
            self.jid_username_map[player] = username

            # Start the game if there are 2 players
            if len(self.jid_username_map) == 2:
                self.start()
                return 100

            return 0

    def get_board(self) -> List[List[int]]:
        return self.board

    def get_turn_name(self) -> str:
        """Returns the name of the player whose turn it is (str)"""
        if self.turn == 1:
            return self.jid_username_map[self.player1]
        return self.jid_username_map[self.player2]

    def get_prev_turn_name(self) -> str:
        """Returns the name of the player whose turn it was last (str)"""
        if self.turn == 1:
            return self.jid_username_map[self.player2]
        return self.jid_username_map[self.player1]

    def get_turn_number(self) -> int:
        """Returns the number of the player whose turn it is (int)"""
        return self.turn

    def get_winner(self) -> str or None:
        """Returns the JID of the winner (str), or None if there is no winner"""
        if self.winner == 1:
            return self.jid_username_map[self.player1]
        elif self.winner == 2:
            return self.jid_username_map[self.player2]
        return None

    def get_players(self) -> Tuple[str, str]:
        """Returns the JIDs of the players (str, str)"""
        return self.player1, self.player2

    def get_game_size(self) -> int:
        """Returns how many in a row is needed (int)"""
        return self.in_a_row

    def play(self, jid: str, location: int) -> int:
        """plays a piece in the given column for the given player

        Args:
            jid (str): jid of the player
            location (int): column to play in

        Returns:
            int:
            0 if the move was successful,
            1 if the game is not running,
            2 if the move is invalid,
            3 if it is not the player's turn,
            4 if the player is not in the game,
            5 if the column is full
            100 if the move was successful and the player won
            101 if the move was successful and the game is a tie
        """
        # convert the location to a 0-indexed column
        location -= 1

        # if the game is not running, return 4
        if not self.game_running:
            return 1

        # if the game is not running, return 1
        if location < 0 or location >= self.x:
            return 2  # Invalid move

        # if the player is not in the game, return 3
        if (jid == self.player1 and self.turn == 2) or (
            jid == self.player2 and self.turn == 1
        ):
            return 3  # Not player's turn

        if jid not in self.jid_username_map:
            return 4  # Player not in game

        # if the player is in the game and it is their turn, play the piece
        if (jid == self.player1 and self.turn == 1) or (
            jid == self.player2 and self.turn == 2
        ):
            # drop the piece in the given column
            # if the move is a winning move, return 100
            # if it's a tie, return 101
            # if the column is full return 5
            # otherwise, return 0
            return self.drop_piece(location)

    def drop_piece(self, col):
        """Drop a piece in the given column for the current player, checking if it is a winning move, and updating the turn if it is not

        returns 100 if the move is a winning move
        returns 101 if the move is a tie
        returns 5 if the column is full
        returns 0 if the move is successful and the game is not over
        """
        # looping from the bottom to the top of the column
        for row in range(self.y - 1, -1, -1):
            if self.board[row][col] == 0:  # if the space is empty
                self.board[row][col] = self.turn  # drop the piece

                # check if the move is a winning move
                if self.check_winner(self.turn, row, col):
                    self.winner = self.turn  # set the winner
                    self.game_running = False  # end the game
                    return 100  # return 100 to indicate a winning move

                # check if the board is full
                elif self.is_full():
                    self.winner = 0  # set the winner to 0 to indicate a tie
                    self.game_running = False  # end the game
                    return 101  # return 101 to indicate a tie

                # if the move is not a winning move, update the turn
                self.turn = 2 if self.turn == 1 else 1

                return 0  # return 0 to indicate a successful move
        return 5  # return 5 to indicate that the column is full

    def check_winner(self, player: str, row: int, col: int) -> bool:
        """Check if the given player has won the game

        Args:
            player (str): player number (1 or 2)
            row (int): row of the last piece played
            col (int): column of the last piece played

        Returns:
            bool: returns True if the player has won, False otherwise
        """

        # check if the player has won in any of the four directions (horizontal, vertical, and both diagonals)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        # loop through each direction
        for dr, dc in directions:
            count = 1  # count the number of pieces in a row

            # Loop over both forward (1) and backward (-1) direction to check for pieces.
            for d in (1, -1):
                # Set up initial row and column for the check in the direction d.
                r = row + dr * d
                c = col + dc * d

                # Continue the loop as long as r and c are inside the board and the piece at board[r][c] belongs to the player.
                while (
                    0 <= r < self.y and 0 <= c < self.x and self.board[r][c] == player
                ):
                    # Increment the count and move the row and column in the direction d.
                    count += 1
                    r += dr * d
                    c += dc * d

            # If the player has won in any direction, return True.
            if count >= self.in_a_row:
                return True
        return False  # If the player has not won in any direction, return False.

    def is_full(self):
        # check if the board is full
        return all(self.board[0][i] != 0 for i in range(self.x))

    def __str__(self):
        # return a string representation of the board
        result = "".join(
            "".join(["🔴" if cell == 1 else "🟡" if cell == 2 else "⚪️" for cell in row])
            + "\n"
            for row in self.board
        )

        column_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        # add the column numbers to the bottom of the board
        if self.x <= 9 and self.x > 0:
            result += "".join(column_numbers[: self.x])

        return result

    def start(self):
        # randomly choose which player goes first
        players = [self.player1, self.player2]
        shuffle(players)
        self.player1, self.player2 = players
        self.game_running = True
