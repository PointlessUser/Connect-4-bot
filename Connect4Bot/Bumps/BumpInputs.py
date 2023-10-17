from kik_unofficial.datatypes.xmpp.chatting import IncomingGroupChatMessage
from .TimerThread import Timer

def process_bump(bumps, chat_message: IncomingGroupChatMessage, bumpResponse):
    
    message = chat_message.body.lower()
    
    if chat_message.group_jid in bumps and (bumps[chat_message.group_jid]["bump"] is True):
            bump = bumps[chat_message.group_jid]
            bump["timer"].reset()
            bump["bumpCount"] = 0
    
    if message == "toggle bump":
        if chat_message.group_jid in bumps:
            bumps[chat_message.group_jid]["bump"] = not bumps[chat_message.group_jid]["bump"]
            if not bumps[chat_message.group_jid]["bump"] :
                return "Bump will not trigger"

            #time = bumps[chat_message.group_jid]["timer"].get_timeout()
            return "Bump will trigger every 60 mins"
        else:
            bumps[chat_message.group_jid] = {"timer":Timer(60*60, bumpResponse), "bumpCount":0, "bump":True,}
        return "Bump will trigger every 60 mins"
    
    elif message.startswith("set bump "):
        print("set bump")
        time = message.split("set bump")[1].strip()
        try:
            time = int(time)
        except ValueError:
            return "Invalid time"
        
        if chat_message.group_jid in bumps and bumps[chat_message.group_jid]["bump"] and time >= 1:
            bumps[chat_message.group_jid]["timer"] = Timer(time*60, bumpResponse)
            if time >= 1:
                bumps[chat_message.group_jid]["timer"] = Timer(time*60, bumpResponse)
                bumps[chat_message.group_jid]["timer"].reset()
                return f"Bump will trigger every {time} min"+("s" if time > 1 else "")
            return "Cannot set bump to less than 1 min"
        else:
            return "Bump is currently disabled"