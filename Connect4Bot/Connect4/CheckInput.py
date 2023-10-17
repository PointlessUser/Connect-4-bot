from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupChatMessage
from .Connect4Game import Connect4Game

from pickle import load, dump

leaderboard_file = 'leaderboard.pkl'
leaderboard = {}

def process_input(games: dict[Connect4Game], chat_message: IncomingGroupChatMessage):
    if action := action_needed(chat_message.body):
        return take_action(games, action, chat_message)
    else:
        return ''
    
def action_needed(message: str):
    """ 
    Returns what needs to be done based on the input message

    Args:
        message (str): sent message
        group_jid (str): group jid
        games (dict): dictionary of games

    Returns:
        int: 
        
    """
    message = message.lower()
    length = len(message)

    # Check if message is a command
    if message == "ping":
        return 1

    # Echo message to group        
    if message.startswith("echo "):
        return 2

    # How to use the bot
    if message == "help":
        return 3

    # leaderboard
    if message in {"leaderboard", "lb"}:
        return 4

    # join/start game (needs display name)
    if (length == 1 and message == "c") or (length == 7 and message == "connect") or (message.startswith('start') and message[5:].strip().isdigit()):
        return 100

    # play move
    if (message.startswith('c') and message[1:].strip().isdigit()) or (message.startswith('connect') and message[7:].strip().isdigit()) or (message.isdigit()):
        return 101

    # Reset game
    if message == 'reset':
        return 102

    # invalid action
    return 0
    
    
        
def take_action(games: dict[Connect4Game], action: int, chat_message: IncomingGroupChatMessage):
    """
    Acts on the action needed
    
        Args:
            action (int): action needed
            chat_message (IncomingGroupChatMessage): chat message
            
        Returns:
            str: what to send to the group (except for 'Display name needed' and 'Invalid action')
    """
    
    message = chat_message.body

    # ping to check if server is running
    if action == 1:
        return "pong"

    # Echo message to group
    if action == 2:
        return message[5:]

    # How to use the bot (help)
    if action == 3:
        return """Commands:
Type C to start/join a game
Type the number to make a move (1-7)
Type reset to reset game
Type 'lb' or 'leaderboard' to see the leaderboard
Type help to see this message
Type 'start #' to start a game with # in a row (e.g. 'start 5' starts connect 5)
Type 'Toggle Bump' to bump the group every hour
Type 'Set Bump #' to set the bump interval to # minutes

Type ping to check if server is running
Type echo to echo a message
Type 'gif (search term)' to send a gif (e.g. 'gif cat' sends a gif of a cat)
"""

    # leaderboard
    if action == 4:
        leaderboard_file = 'leaderboard.pkl'
        try:
            leaderboard = load(open(leaderboard_file, 'rb'))
        except Exception:
            leaderboard = {}
            return "The leaderboard is empty"
        
        leaderboard_sorted = sorted(leaderboard.items(), key=lambda x: x[1][1], reverse=True)
        leaderboard_string = "Leaderboard:\n"
        for i, score in enumerate(leaderboard_sorted):
            leaderboard_string += f"{i + 1}: {score[1][0]} ({score[1][1]})\n"
        
        return leaderboard_string
        
        

    # join/start game (needs display name)
    if action == 100:
        return 'Display name needed'

    # play move
    if action == 101:
        message = message.lower()
        if message.startswith('c') and message[1:].strip().isdigit():
            move = int(message[1:].strip())
        elif message.startswith('connect') and message[7:].strip().isdigit():
            move = int(message[7:].strip())
        elif message.isdigit():
            if (chat_message.group_jid in games) and (chat_message.from_jid not in games[chat_message.group_jid].get_players()):
                return 'Invalid action'
            move = int(message)

        return play_move(move, games, chat_message)

    if action == 102:
        return reset_game(games, chat_message.group_jid)

    # invalid action
    return 'Invalid action'
        


def play_move(move, games: dict[Connect4Game], chat_message: IncomingGroupChatMessage):
    """plays a move in the game

    Args:
        move (int): what column to play in
        games (dict[Connect4Game]): dictionary of games
        chat_message (IncomingGroupChatMessage): chat message received from group

    Returns:
        str: message to send to group
    """
    
    group_jid = chat_message.group_jid
    player_jid = chat_message.from_jid

    # check if game exists
    if group_jid in games:
        game: Connect4Game = games[group_jid]
    elif not chat_message.body.lower().startswith("connect"):
        return "No game in progress"

    # play move
    response = game.play(player_jid, move)

    # move was valid
    if response == 0:
        if game.turn == 1:
            return game.__str__(), f"🔴 {game.get_turn_name()}'s turn 🔴"
        else:
            return game.__str__(), f"🔵 {game.get_turn_name()}'s turn 🔵"

    # no game in progress
    elif response == 1:
        if not chat_message.body.lower().startswith("connect"):
            return "No game in progress"

    # invalid move (out of bounds)
    elif response == 2:
        return "Invalid move"

    # not your turn
    elif response == 3:
        return "Not your turn"

    # not your game
    elif response == 4:
        return "You are not in this game!"

    # The column is full
    elif response == 5:
        return "Column is full"

    # Game ended successfully
    elif response == 100:
        leaderboard_file = 'leaderboard.pkl'
        games.pop(group_jid)
        try:
            leaderboard = load(open(leaderboard_file, 'rb'))
        except Exception:
            leaderboard = {}
            dump(leaderboard, open(leaderboard_file, 'wb'))

        if game.get_winner() in leaderboard:
            leaderboard[game.get_winner()][0] = game.get_winner_name()
            leaderboard[game.get_winner()][1] += 1
        else:
            leaderboard[game.get_winner()] = [game.get_winner_name(), 1]

        dump(leaderboard, open(leaderboard_file, 'wb'))
        return game.__str__(), f"{game.get_winner_name()} won!"

    # Game ended in a draw
    elif response == 101:
        return game.__str__(), "Game ended in a draw"


def reset_game(games: dict[Connect4Game] ,group_jid: str):
    """resets the game if its in progress

    Args:
        games (dict[Connect4Game]): dictionary of games
        group_jid (str): group jid

    Returns:
        str: message to send to group
    """
    
    if group_jid in games:
        games.pop(group_jid)
        return "Game Reset"
    else:
        return "No game in progress"


def start_game(games: dict[Connect4Game], display_name: str, chat_message: IncomingGroupChatMessage):
    # start game if not already started
    group_jid = chat_message.group_jid
    player_jid = chat_message.from_jid
    message = chat_message.body
    message = message.lower()
    
    game_type = 4
    
    if message.startswith('start') and message[5:].strip().isdigit():
        game_type = int(message[5:].strip())

    # check if game exists, if not, create one
    if group_jid not in games:
        games[group_jid] = Connect4Game(in_a_row=game_type)

    # store the game into a variable
    game: Connect4Game = games[group_jid]

    # add player to game
    if (response := game.addPlayer(player_jid, display_name)) == 0:
        return (f"Connect {game.in_a_row} started", f"{display_name} joined, type \"C\" to join")

    # player already in game
    elif response == 1:
        return "Player already in game"

    # game already in progress
    elif response == 2:
        return "Game already in progress"

    # game started successfully
    elif response == 100:
        return game.__str__(), f"🔴 {game.get_turn_name()}'s turn 🔴"

    else:
        return "Invalid game type"

# add return game board as a function