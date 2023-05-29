import logging
import sys

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

from Bumps.BumpInputs import process_bump
from Bumps.bumpQuotes import getQuote
from Connect4.CheckInput import *

username = "username"
password = "password"

bumpTime = 60 * 60  # 1 hour

games = {}  # Map of JID to Connect4Game
bumps = {}  # Map of JID to number of bumps


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

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        # self.client.request_roster()

    def bump(self, bumpJID):
        print("Bump")
        if bumpJID in bumps and bumps[bumpJID]["bump"]:
            bump = bumps[bumpJID]
            self.client.send_chat_message(bumpJID, getQuote(bump['bumpCount']))
            bump["bumpCount"] += 1
            bump["timer"].reset()
            

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        """Called when a group chat message is received"""
        # reset timer if message is from bump group
        
        self.senderJID = chat_message.from_jid
        self.senderName = chat_message.from_jid.split('@')[0]
        self.groupJID = chat_message.group_jid
            
        # process bumps
        if output := process_bump(bumps, chat_message, partial(self.bump, chat_message.group_jid)):
            self.client.send_chat_message(chat_message.group_jid, output)
        
        # process connect4 game input
        output = process_input(games, chat_message)
        
        # if display name is needed, get it
        if output == 'Display name needed':
            self.chat_message = chat_message
            self.client.xiphias_get_users_by_alias([chat_message.from_jid])
        
        # if message isnt invalid action or display name needed, send message
        elif output != '':
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
            name = user.display_name

            if name is None:
                name = self.senderName
                
            # get first name    
            name = name.split()[0]
            
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
