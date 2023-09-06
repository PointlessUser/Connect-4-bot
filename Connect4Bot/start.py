import os
import yaml

from functools import partial

from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse
from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupChatMessage


from Bumps.BumpInputs import process_bump
from Bumps.bumpQuotes import getQuote
from Connect4.CheckInput import *


bumpTime = 60 * 60  # 1 hour

games = {}  # Map of JID to Connect4Game
bumps = {}  # Map of JID to number of bumps

def main():
    # The credentials file where you store the bot's login information
    creds_file = "creds.yaml"
        
    # Changes the current working directory to Connect4Bot if it isn't already
    if not os.path.isfile(creds_file):
        os.chdir("Connect4Bot")
    
    # load the bot's credentials from creds.yaml if it exists, otherwise ask for them for their login information
    try:
        with open(creds_file) as f:
            creds = yaml.safe_load(f)
    except FileNotFoundError:
        creds = {'Username': input("Username: "), 'Password': input("Password: ")}
    
    bot = Connect4Bot(creds)


class Connect4Bot(KikClientCallback):
    def __init__(self, creds: dict):
        
        username = creds["username"]
        password = creds.get("password") or input("Password: ")
        kik_node = creds.get("node")
        device_id = creds.get("device_id")
        android_id = creds.get("android_id")
        self.tenor_key = creds.get("tenor_key")
        
        self.senderJID = None
        self.senderName = None
        self.groupJID = None

        # start bot
        self.client = KikClient(self, username, password, kik_node, device_id, android_id, logging=True)
        # self.client = KikClient(self, username, password, logging=True)
        self.client.wait_for_messages()
    

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
                
        if chat_message.body.lower().startswith("gif "):
            print("Sending gif")
            self.client.send_gif_image(chat_message.group_jid, chat_message.body[4:], self.tenor_key)

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
    
    def on_disconnected(self):
        print("Bot disconnected.")
        


if __name__ == "__main__":
    main()
