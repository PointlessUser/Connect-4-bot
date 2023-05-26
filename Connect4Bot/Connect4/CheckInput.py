from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupChatMessage
from .Connect4Game import Connect4Game


def process_input(games: dict[Connect4Game], chat_message: IncomingGroupChatMessage):
    
    action = action_needed(chat_message.body)
    return take_action(games, action, chat_message)



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
    print(message)
    
    # Check if message is a command
    if message == "ping":
        return 1
    
    # Echo message to group        
    if message.startswith("echo "):
        return 2
    
    # How to use the bot
    if message == "help":
        return 3
    
    # join/start game (needs display name)
    if (length == 1 and message == "c") or (length == 7 and message == "connect") or (message.startswith('start') and message[5:].strip().isdigit()):
        return 100
    
    
    if (message.startswith('c') and message[1:].strip().isdigit()) or (message.startswith('connect') and message[7:].strip().isdigit()):
        return 101
    
    # Reset game
    if message== 'reset':
        return 102
    
    
    
        
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
    
    # How to use the bot
    if action == 3:
        return """Commands:
connect or C to join game
(connect #) or (C#) to make a move
(example: connect 1 or C2)
reset to reset game
ping to check if server is running
echo to echo message
"""

    # join/start game (needs display name)
    if action == 100:
        return 'Display name needed'
    
    # play move
    if action == 101:
        return play_move(message, games, chat_message)
    
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
    else:
        return "No game in progress"

    # play move
    response = game.play(player_jid, move)

    # move was valid
    if response == 0:
        return game.__str__(), f"{game.get_turn_name()}'s turn"

    # no game in progress
    elif response == 1:
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
        games.pop(group_jid)
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
        f"Connect {game.in_a_row} started"
        return f"{display_name} joined, Type Connect to join"

    # player already in game
    elif response == 1:
        return "Player already in game"

    # game already in progress
    elif response == 2:
        return "Game already in progress"

    elif response == 100:
        return game.__str__(), f"{game.get_turn_name()}'s turn"

    else:
        return "Invalid game type"