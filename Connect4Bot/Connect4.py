import argparse
import logging
import sys
import time
import threading
from random import shuffle

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

username = "Connect4Bot_"
password = ""

games = {}


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = Connect4Bot()


class Connect4Bot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)
        self.client.wait_for_messages()

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        print(f"{jid_to_username(chat_message.from_jid)}: {chat_message.body}")
        group_jid = chat_message.group_jid
        message_sender = jid_to_username(chat_message.from_jid)

        if chat_message.body.lower() == "reset":
            games.pop(group_jid)
            self.client.send_chat_message(group_jid, "Game Reset")

        if startGame(chat_message.body):
            if group_jid not in games:
                games[group_jid] = Connect4Game(player1=chat_message.from_jid)
                self.client.send_chat_message(
                    group_jid,
                    f"{message_sender} joined, Type Connect to join",
                )
            else:
                game = games[group_jid]
                if game.player2 is None and game.player1 != chat_message.from_jid:
                    game.player2 = chat_message.from_jid
                    self.client.send_chat_message(group_jid, game.__str__())
                    game.start()
                    self.client.send_chat_message(
                        group_jid, f"{message_sender}'s turn'"
                    )

                else:
                    if game.player1 != chat_message.from_jid:
                        self.client.send_chat_message(
                            group_jid, "You are already in the game"
                        )
                    self.client.send_chat_message(group_jid, "Game already in progress")

        elif (move := gameMove(chat_message.body)) != -1:
            print("move detected")
            if group_jid in games:
                game = games[group_jid]
                if (
                    game.game_running
                    and chat_message.from_jid
                    == game.get_players()[game.get_turn_number() - 1]
                ):
                    if game.play(move):
                        self.client.send_chat_message(group_jid, game.__str__())
                        self.client.send_chat_message(
                            group_jid, f"{game.get_prev_turn()} played at {move}"
                        )
                        if game.winner:
                            self.client.send_chat_message(
                                group_jid, f"{game.get_winner()} won!"
                            )
                            del games[group_jid]
                        elif game.is_full():
                            self.client.send_chat_message(
                                group_jid, "Game ended in a draw"
                            )
                            del games[group_jid]
                    else:
                        self.client.send_chat_message(group_jid, "Invalid move")

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print(f"[-] Connection failed: {response.message}")

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print(f"[-] Register error: {response.message}")


def jid_to_username(jid):
    return jid.split("@")[0][:-4]


def startGame(message: str):
    message = message.split()

    return False if len(message) > 1 else message[0].lower() in ["c", "connect"]


def gameMove(message: str):
    message = message.split()

    if len(message) != 2:
        return -1

    if message[0].lower() not in ["c", "connect"]:
        return -1

    return int(message[1]) if message[1].isdigit() else -1


class Connect4Game:
    def __init__(self, player1=None, player2=None, in_a_row=4):
        self.in_a_row = in_a_row
        self.x = in_a_row * 2 - 1
        self.y = in_a_row + 2
        self.board = [[0 for _ in range(self.x)] for _ in range(self.y)]
        self.player1 = player1
        self.player2 = player2
        self.turn = 1
        self.winner = None
        self.game_running = False

    def get_board(self):
        return self.board

    def get_turn(self):
        if self.turn == 1:
            return jid_to_username(self.player1)
        else:
            return jid_to_username(self.player2)

    def get_prev_turn(self):
        if self.turn == 1:
            return jid_to_username(self.player2)
        else:
            return jid_to_username(self.player1)

    def get_turn_number(self):
        return self.turn

    def get_winner(self):
        return jid_to_username(self.winner)

    def get_players(self):
        return self.player1, self.player2

    def get_in_a_row(self):
        return self.in_a_row

    def play(self, location):
        location -= 1
        if location < 0 or location >= self.x:
            return False

        for i in range(self.y - 1, -1, -1):
            if self.board[i][location] == 0:
                self.board[i][location] = self.turn
                if self.check_winner(self.turn, i, location):
                    self.winner = self.player1 if self.turn == 1 else self.player2
                self.turn = 1 if self.turn == 2 else 2
                return True
        return False

    def check_winner(self, player, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for d in (1, -1):
                r, c = row + dr * d, col + dc * d
                while (
                    0 <= r < self.y and 0 <= c < self.x and self.board[r][c] == player
                ):
                    count += 1
                    r += dr * d
                    c += dc * d

            if count >= self.in_a_row:
                return True
        return False

    def is_full(self):
        return all(self.board[0][i] != 0 for i in range(self.x))

    def __str__(self):
        result = "".join(
            "".join(["🔴" if cell == 1 else "🟡" if cell == 2 else "⚪️" for cell in row])
            + "\n"
            for row in self.board
        )
        result += "-" * (self.x * 2 - 1)
        return result

    def start(self):
        players = [self.player1, self.player2]
        shuffle(players)
        self.player1, self.player2 = players
        self.game_running = True


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
