from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupChatMessage
from .TimerThread import Timer

def process_bump(bumps, chat_message: IncomingGroupChatMessage, bumpResponse):
    
    message = chat_message.body.lower()
    
    if chat_message.group_jid in bumps and (bumps[chat_message.group_jid]["bump"] is True) and message != "toggle bump":
            bump = bumps[chat_message.group_jid]
            bump["timer"].reset()
            bump["bumpCount"] = 0
            return ''
    

    if message == "toggle bump":
        if chat_message.group_jid in bumps:
            bumps[chat_message.group_jid]["bump"] = not bumps[chat_message.group_jid]["bump"]
            if not bumps[chat_message.group_jid]:
                return "Bump will not trigger"

            #time = bumps[chat_message.group_jid]["timer"].get_timeout()
            return "Bump will trigger every 60 mins"
        else:
            bumps[chat_message.group_jid] = {"timer":Timer(60*60, bumpResponse), "bumpCount":0, "bump":True,}
        return "Bump will trigger every 60 mins"
