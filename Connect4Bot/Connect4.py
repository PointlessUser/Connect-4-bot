import argparse
import logging
import sys
import time
import threading
from random import shuffle
from connect4_game.Connect4Game import Connect4Game
from bumpQuotes.bumpQuotes import getQuote
from functools import partial
from connect4_game.CheckInput import *

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
bumpResponse = "Yay someone talked!" 

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
                False
            ],
            # friend
            "1100253900967_g@groups.kik.com": [
                Timer(bumpTime, partial(self.bump, "1100253900967_g@groups.kik.com")),
                0,
                False,
            ],
        }

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        # self.client.request_roster()

    def bump(self, bumpJID):
        print("Bump")
        if bumpJID in self.bumpJIDs:
            self.bumpJIDs[bumpJID][1] += 1
            self.bumpJIDs[bumpJID][2] = True
            self.client.send_chat_message(bumpJID, getQuote(self.bumpJIDs[bumpJID][1]))
            self.bumpJIDs[bumpJID][0].reset()
            

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        """Called when a group chat message is received"""
        # reset timer if message is from bump group
        if chat_message.group_jid in self.bumpJIDs:
            timer = self.bumpJIDs[chat_message.group_jid][0]
            timer.reset()
            if self.bumpJIDs[chat_message.group_jid][2]:
                self.client.send_chat_message(chat_message.group_jid, bumpResponse)
                self.bumpJIDs[chat_message.group_jid][2] = False
            self.bumpJIDs[chat_message.group_jid][1] = 0

        self.senderJID = chat_message.from_jid
        self.groupJID = chat_message.group_jid
        self.message = chat_message.body
        self.senderName = jid_to_username(self.senderJID)
        
        output = process_input(games, chat_message)
        
        if output == 'Display name needed':
            self.chat_message = chat_message
            print("here2")
            self.client.xiphias_get_users_by_alias([chat_message.from_jid])
        elif output != 'Invalid action':
            if type(output) is tuple:
                for msg in output:
                    self.client.send_chat_message(chat_message.group_jid, msg)
            else:
                self.client.send_chat_message(chat_message.group_jid, output)

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

            response = start_game(games, name, self.chat_message)
            if type(response) is tuple:
                for msg in response:
                    self.client.send_chat_message(self.groupJID, msg)
            else:
                self.client.send_chat_message(self.groupJID, response)

            
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
