import sys
import os
import pytest

# caution: path[0] is reserved for script path (or '' in REPL)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)

sys.path.insert(1, f"{PARENT_DIR}/Connect4Bot")

from Connect4_game import Connect4Game


def test_init():
    # Test initial configuration of the game
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    # Check if the correct players are set
    assert game.get_players() in [("p1_jid", "p2_jid"), ("p2_jid", "p1_jid")]
    # The turn number at the start of the game should be 1
    assert game.get_turn_number() == 1
    # The player whose turn it is should be one of the two players
    assert game.get_turn_name() in ("p1_name", "p2_name")
    # The game size for Connect4 should be 4
    assert game.get_game_size() == 4
    # There should be no winner at the start of the game
    assert game.get_winner() is None


def test_addPlayer():
    # Test adding players to the game
    game = Connect4Game()
    # Adding first player should return 0 (success)
    assert game.addPlayer("p1_jid", "p1_name") == 0
    # Trying to add the same player again should return 1 (player already added)
    assert game.addPlayer("p1_jid", "p1_name") == 1
    # Adding second player should return 0 (Game is starting)
    assert game.addPlayer("p2_jid", "p2_name") == 100
    # Trying to add a third player should return 2 (game is full)
    assert game.addPlayer("p3_jid", "p3_name") == 2


def test_get_board():
    # Test the functionality of get_board method
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    # Check the default Connect4 board dimensions
    assert len(game.get_board()) == 6
    assert len(game.get_board()[0]) == 7


def test_play():
    # Test the play method
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    player1, player2 = game.get_players()

    # A correct move by the right player should return 0
    assert game.play(player1, 1) == 0
    # Trying to play when it's not the player's turn should return 3
    assert game.play(player1, 1) == 3
    # A correct move by the right player should return 0
    assert game.play(player2, 1) == 0
    # Trying to play when it's not the player's turn should return 3
    assert game.play(player2, 1) == 3
    # A correct move by the right player should return 0
    assert game.play(player1, 1) == 0
    # Trying to play as a non-existent player should return 4
    assert game.play("p3_jid", 1) == 4
    # Trying to play in an invalid column should return 2
    assert game.play(player2, 10) == 2
    assert game.play(player2, -1) == 2

    # A correct move by the right player should return 0
    assert game.play(player2, 1) == 0


@pytest.mark.parametrize(
    "moves,expected_result",
    [
        # Connect 4 in the first column
        [(1, 1, 2, 1, 2, 1, 2, 1), 100],
        # Connect 4 horizontally
        [(2, 2, 3, 2, 3, 2, 1, 1, 4), 100],
        # Connect 4 diagonally from bottom-left to top-right
        [(1, 2, 1, 3, 1, 1, 3, 3, 4, 2, 2, 4, 4, 3, 3, 1, 5, 2), 100],
        # Connect 4 diagonally from top-left to bottom-right
        [(4, 3, 4, 2, 4, 4, 2, 2, 1, 3, 3, 1, 1, 1, 2, 3, 5), 100],
        # Connect 4 drawn game
        [(4, 3, 2, 1, 5, 6, 7, 6, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 7, 6, 6, 7, 4, 5, 3, 4, 2, 2, 3, 1, 5, 6, 7, 7, 7, 6, 5, 4, 3, 2, 1, 1), 101]
    ],
)
def test_winning(moves, expected_result):
    # Test winning conditions
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    player1, player2 = game.get_players()

    # Play the moves
    for i, move in enumerate(moves[:-1]):
        if game.turn == 1:
            assert game.play(player1, move) == 0
        else:
            assert game.play(player2, move) == 0

    # The last move should be the winning move
    move = moves[-1]
    i += 1
    player = player1 if game.turn == 1 else player2

    # The winning move should return the expected result
    assert game.play(player, move) == expected_result

    # The game should be over

    # The player who connected 4 should be the winner
    if expected_result == 100:
        assert game.get_winner() == player
    else:
        assert game.get_winner() is None


def test_full_column():
    # Test the scenario where a column is full
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])

    player1, player2 = game.get_players()

    for _ in range(3):
        assert game.play(player1, 5) == 0
        assert game.play(player2, 5) == 0
    # Trying to play in a full column should return 5
    assert game.play(player1, 5) == 5
