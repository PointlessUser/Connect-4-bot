import argparse
import logging
import sys
import time
import threading
from random import shuffle
from Connect4_game import Connect4Game
from bumpQuotes import getQuote
from functools import partial

from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.datatypes.xmpp.sign_up import (
    RegisterResponse,
    UsernameUniquenessResponse,
)
from kik_unofficial.datatypes.xmpp.chatting import (
    IncomingChatMessage,
    IncomingGroupChatMessage,
    IncomingStatusResponse,
    IncomingGroupStatus,
)

from TimerThread import Timer

username = "Username"
password = "Password"

bumpTime = 60 * 60  # 1 hour

games = {}  # Map of JID to Connect4Game


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    # bot = Connect4Bot()
    Connect4Bot()


class Connect4Bot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)
        self.client.wait_for_messages()

        self.senderJID = None
        self.senderName = None
        self.groupJID = None
        self.bumpJIDs = {
            # mine
            "1100254805149_g@groups.kik.com": [
                Timer(bumpTime, partial(self.bump, "1100254805149_g@groups.kik.com")),
                0,
            ],
            # friend
            "1100253900967_g@groups.kik.com": [
                Timer(bumpTime, partial(self.bump, "1100253900967_g@groups.kik.com")),
                0,
            ],
        }

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        # self.client.request_roster()

    def bump(self, bumpJID):
        print("Bump")
        if bumpJID in self.bumpJIDs:
            self.bumpJIDs[bumpJID][1] += 1
            self.client.send_chat_message(bumpJID, getQuote(self.bumpJIDs[bumpJID][1]))
            self.bumpJIDs[bumpJID][0].reset()

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        """Called when a group chat message is received"""

        # reset timer if message is from bump group
        if chat_message.group_jid in self.bumpJIDs:
            timer = self.bumpJIDs[chat_message.group_jid][0]
            timer.reset()

            self.bumpJIDs[chat_message.group_jid][1] = 0

        self.senderJID = chat_message.from_jid
        self.groupJID = chat_message.group_jid
        self.message = chat_message.body
        self.senderName = jid_to_username(self.senderJID)
        # get display name of the user who sent the message
        getDisplayName = not self.processMessage(
            self.message, self.senderJID, self.groupJID
        )
        if getDisplayName:
            self.client.xiphias_get_users_by_alias([chat_message.from_jid])

    def processDisplayNameMessage(self, message, playerJID, playerName, groupJID):
        message = message.lower()
        message = message.strip()

        # player is joining a game
        if message in ["c", "connect"]:
            self.startGame(playerJID, playerName, groupJID)
            return True

        message = message.split()

        if len(message) == 2 and (message[0] == "start" and message[1].isdigit()):
            self.startGame(playerJID, playerName, groupJID, int(message[1]))
            return True

    def processMessage(self, message, playerJID, groupJID):
        message = message.lower()
        message = message.strip()

        # check if message
        if message == "reset":
            if groupJID in games:
                games.pop(groupJID)
                self.client.send_chat_message(groupJID, "Game Reset")
            else:
                self.client.send_chat_message(groupJID, "No game to reset")
            return True

        # display help message
        if message == "help":
            self.client.send_chat_message(
                groupJID,
                """Commands: 
connect or C to join game
connect # or C # to make a move
reset to reset game
ping to check if server is running
help to display this message
""",
            )
            return True

        # check if server is running
        elif message == "ping":
            self.client.send_chat_message(groupJID, "pong")
            return True

        # player is joining a game
        elif message in ["c", "connect"]:
            return False

        # player is making a move
        else:
            message = message.split()

            # check if message is a move
            if len(message) == 2 and (
                message[0] in ["c", "connect"] and message[1].isdigit()
            ):
                move = int(message[1])
                self.playMove(move, playerJID, groupJID)
                return True

            if len(message) == 2 and (message[0] == "start" and message[1].isdigit()):
                return False

            # check if message is a move
            elif len(message) == 1:
                message = message[0]
                m1 = message.split("c")
                m2 = message.split("connect")

                if len(m1) == 2 and m1[1].isdigit():
                    move = int(m1[1])
                    self.playMove(move, playerJID, groupJID)

                elif len(m2) == 2 and m2[1].isdigit():
                    move = int(m2[1])
                    self.playMove(move, playerJID, groupJID)
                return True

        return True

    def startGame(self, playerJID, playerName, groupJID, gameType=4):
        # start game if not already started

        # check if game exists, if not, create one
        if groupJID not in games:
            games[groupJID] = Connect4Game(in_a_row=gameType)
            self.client.send_chat_message(groupJID, f"Connect {gameType} initiated")

        game = games[groupJID]

        # add player to game
        if (response := game.addPlayer(playerJID, playerName)) == 0:
            self.client.send_chat_message(
                groupJID, f"{playerName} joined, Type Connect to join"
            )
            return True

        # player already in game
        elif response == 1:
            self.client.send_chat_message(groupJID, "Player already in game")

        # game already in progress
        elif response == 2:
            self.client.send_chat_message(groupJID, "Game already in progress")

        elif response == 100:
            self.client.send_chat_message(groupJID, game.__str__())
            self.client.send_chat_message(groupJID, f"{game.get_turn_name()}'s turn")

        else:
            self.client.send_chat_message(groupJID, "Invalid game type")

        return False

    def playMove(self, move, playerJID, groupJID):
        # check if game exists
        if groupJID in games:
            game = games[groupJID]
        else:
            self.client.send_chat_message(groupJID, "No game in progress")
            return

        # play move
        response = game.play(playerJID, move)

        # move was valid
        if response == 0:
            self.client.send_chat_message(groupJID, game.__str__())
            self.client.send_chat_message(groupJID, f"{game.get_turn_name()}'s turn")

        # no game in progress
        elif response == 1:
            self.client.send_chat_message(groupJID, "No game in progress")

        # invalid move (out of bounds)
        elif response == 2:
            self.client.send_chat_message(groupJID, "Invalid move")

        # not your turn
        elif response == 3:
            self.client.send_chat_message(groupJID, "Not your turn")

        # not your game
        elif response == 4:
            self.client.send_chat_message(groupJID, "You are not in this game!")

        # The column is full
        elif response == 5:
            self.client.send_chat_message(groupJID, "Column is full")

        # Game ended successfully
        elif response == 100:
            self.client.send_chat_message(groupJID, game.__str__())
            self.client.send_chat_message(groupJID, f"{game.get_winner_name()} won!")
            games.pop(groupJID)

        # Game ended in a draw
        elif response == 101:
            self.client.send_chat_message(groupJID, game.__str__())
            self.client.send_chat_message(groupJID, "Game ended in a draw")
            games.pop(groupJID)

    def resetGame(self, group_jid):
        games.pop(group_jid)
        self.client.send_chat_message(group_jid, "Game Reset")

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print(f"[-] Connection failed: {response.message}")

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print(f"[-] Register error: {response.message}")

    def on_xiphias_get_users_response(self, response):
        for user in response.users:
            jid = user.alias_jid or user.jid
            name = user.display_name

            if name is None:
                name = self.senderName

            self.processDisplayNameMessage(
                self.message, self.senderJID, name, self.groupJID
            )

            # print(f"Display name for {jid} = {name}")


def jid_to_username(jid):
    return jid.split("@")[0][:-4]


if __name__ == "__main__":
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the client
    callback = Connect4Bot()
    client = KikClient(callback=callback, kik_username=username, kik_password=password)
    client.wait_for_messages()
