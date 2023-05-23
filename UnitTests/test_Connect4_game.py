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
    assert game.get_players() == ("p1_jid", "p2_jid")
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

    if game.get_turn_name() == "p1_name":
        player1 = "p1_jid"
        player2 = "p2_jid"
    else:
        player1 = "p2_jid"
        player2 = "p1_jid"

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
        [(1, 1, 2, 1, 2, 1, 1), 0],
        # Connect 4 in the second column
        [(2, 2, 3, 2, 3, 2, 2), 0],
        # Connect 4 diagonally from bottom-left to top-right
        [(1, 2, 1, 3, 1, 1, 3, 3, 4, 2, 2, 4, 4), 0],
        # Connect 4 diagonally from top-left to bottom-right
        [(4, 3, 4, 2, 4, 4, 2, 2, 1, 3, 3, 1, 1), 0],
    ],
)
def test_winning(moves, expected_result):
    # Test winning conditions
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    for move in moves:
        assert (
            game.play("p1_jid" if game.get_turn_name() == "p1_name" else "p2_jid", move)
            == expected_result
        )
    # The player who connected 4 should be the winner
    assert game.get_winner() == ("p1_name" if moves.count(1) % 2 == 0 else "p2_name")


def test_full_column():
    # Test the scenario where a column is full
    game = Connect4Game(player1=["p1_jid", "p1_name"], player2=["p2_jid", "p2_name"])
    for _ in range(3):
        assert game.play("p1_jid", 5) == 0
        assert game.play("p2_jid", 5) == 0
    assert game.play("p1_jid", 5) == 0
    # Trying to play in a full column should return 101
    assert game.play("p2_jid", 5) == 101