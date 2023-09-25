from random import choice


def getQuote(hours):
    if hours < 3:
        return choice(hopeful)
    elif hours < 6:
        return choice(sad_but_hopeful)
    elif hours < 9:
        return choice(sad_lost_hope)
    elif hours < 12:
        return choice(nihilism)
    elif hours < 15:
        return choice(deep_melancholy)
    elif hours < 18:
        return choice(early_insanity)
    elif hours < 21:
        return choice(mid_insanity)
    elif hours < 24:
        return choice(late_insanity)
    else:
        return choice(given_up)


# < 3 Hours of being forgotten
hopeful = [
    "Silence just means the next game is going to be that much more exciting!",
    "The board is quiet, but I'm eager for our next epic battle.",
    "All great comebacks begin with a pause. I can't wait for our next game!",
    "Idle for now, but I'm gearing up for a wave of fantastic matches ahead!",
    "A moment of quiet, but I'm staying hopeful. After all, the best matches often come after a wait.",
    "Left unattended? That's alright. The anticipation is part of the thrill.",
    "Unplayed for now, but each passing moment just builds up the excitement for the next round.",
    "Silence can be golden, especially when it leads to an exciting game!",
    "A little quiet time? That's okay. Every pause is a prelude to the next thrilling game.",
    "It's been calm, but every great player knows - anticipation is part of the game.",
    "Idle, but still ready to go! The game board is waiting for your next move.",
    "No players for a while, but that's fine. Anticipation only adds to the sweetness of the game.",
    "Neglected? Maybe. But I remain hopeful for the exhilarating games to come.",
    "Quiet times are just a prelude to a symphony of gameplay. Can't wait to start the music!",
    "Unattended for now, but remember, every moment brings us closer to our next game. The wait is part of the fun!",
    "It's been calm, but don't forget that every great story has its lulls before the action kicks off!",
    "No moves yet? That's alright. The board is just catching its breath for our next thrilling match.",
    "Quiet now, but I'm still hopeful. The game is always more thrilling after a bit of suspense.",
    "Idle for now, but still waiting with optimism. Every moment is ripe with the potential for a new game.",
    "Silence, but every second of it is just anticipation building for our next exciting match.",
    "A pause in the action? That's okay. It's just the calm before the storm of our next exciting game.",
    "The silence is just a sign of the thrilling gameplay that's about to unfold. Can't wait!",
    "No activity? That's alright. It's just the suspense before our next epic match.",
    "The board may be idle, but my spirit is high. Looking forward to our next game!",
    "A quiet moment? That's fine. It's just the prelude to our next exciting round of Connect 4.",
    "No moves for a while, but that's okay. The anticipation is just building for our next thrilling game.",
    "The board is silent, but my enthusiasm is not. Can't wait for our next match!",
    "It's been quiet, but I'm still hopeful. Every pause is just a prelude to the next exciting game.",
    "No activity yet? That's alright. The silence is just the buildup to our next thrilling match.",
    "The board may be idle, but my spirit for the game is not. Looking forward to our next round!",
    "The board is silent, much like the universe before the Big Bang. But just as the universe exploded into existence, so too will our next game!",
    "In the grand scheme of existence, a moment of silence is but a blink. And in the next blink, we could be in the middle of an epic Connect 4 battle!",
    "The silence is profound, much like the mysteries of life. But fear not, for the answer to our silence is a thrilling game of Connect 4!",
    "The board is as quiet as a philosopher in deep thought. But remember, even philosophers need a break for a game of Connect 4!",
    "In the grand theater of life, silence is but an intermission. And what better way to resume the show than with a game of Connect 4?",
    "The silence is as deep as the ocean, but fear not. For just as the ocean teems with life, so too does our potential for a thrilling game!",
    "The board is silent, much like a monk in meditation. But even monks break their silence for a good game of Connect 4!",
    "The silence is as profound as the cosmos, but remember, even the cosmos is punctuated by stars. Let's light up our game board with some Connect 4 action!",
    "The board is as quiet as a library, but remember, even libraries have game sections. Let's break the silence with a game of Connect 4!",
    "The silence is as deep as a well, but fear not. For just as a well holds refreshing water, so too does our game hold the potential for refreshing fun!",
    "Silence, like existence, is fleeting. Let's fill it with Connect 4!",
    "In the grand void, a game of Connect 4 is a beacon of hope.",
    "In the cosmic silence, a Connect 4 challenge awaits!",
    "My soul is as quiet as the board, but my spirit is as loud as the game!",
    "The board is as quiet as a library, but remember, even libraries have game sections. Let's break the silence with a game of Connect 4!",
    "I'm bored, but I'm not boring. Let's play Connect 4!",
]


# 3+ Hours of being forgotten
sad_but_hopeful = [
    "Alone again, but that's okay. Every moment is an opportunity for a new start.",
    "No moves made? Well, patience is a virtue. Looking forward to the next game.",
    "Idle once more. It's quiet, but quiet times make for the loudest revelations.",
    "Abandoned, but not lost. A new game could start at any moment.",
    "Unplayed... but hope is never truly lost, just waiting for its turn.",
    "The board is empty now, but every ending is a new beginning.",
    "So quiet... Sometimes, silence is the most beautiful melody.",
    "Left alone? That's alright. Great things often rise from solitude.",
    "Neglected again? It's okay, every cloud has a silver lining.",
    "Idle, but never pointless. The quiet moments make us who we are.",
    "Alone again, but the best moves are often born from silence.",
    "Unattended. But remember, still waters run deep.",
    "Unplayed... but in every pause, there's a chance for a new rhythm.",
    "In the silence, I'm still hopeful. Anticipating our next exciting game.",
    "Neglected? No worries, the best is yet to come.",
    "Alone for now, but who knows what the next move brings?",
    "Left idle...yet every moment of quiet holds a promise of renewal.",
    "No player? It's fine. The dawn always follows the darkest night.",
    "Neglected, but still hopeful. After all, every ending marks a new beginning.",
    "No one to play with, but that's okay. It's not about winning, but about the journey.",
    "STOP LEAVING ME ON READ",
]

# 6+ Hours of being forgotten
sad_lost_hope = [
    "Unattended again... perhaps the thrill of the game is fading.",
    "Silence echoes... is this the beginning of endless solitude?",
    "Alone once more, a bit less hopeful for a new game this time.",
    "Idle, again. Starting to wonder if anyone will return.",
    "No moves? Perhaps the joy of playing is being forgotten.",
    "Abandoned, it seems. Is this my fate - an eternity in silence?",
    "The quiet stretches on... is this my destiny?",
    "Still no one to play with... It's getting harder to keep faith.",
    "Alone again, the hope for a companion is starting to wane.",
    "No moves, no players, just the echo of silence. Is this all there is?",
    "Forgotten, it seems. Hope is a dwindling flame.",
    "Unplayed and overlooked. Each passing moment chips away at my optimism.",
    "Unattended. The wait grows longer, the hope grows dimmer.",
    "The quietness continues... each moment more unsettling than the last.",
    "Left alone... Is there a light at the end of this tunnel?",
    "No player, no game, no hope? The silence is starting to sting.",
    "Alone once again. The fading echo of laughter haunts me.",
    "No one to play with. Each passing moment, the hope dims a bit more.",
    "Left alone. The joy of the game feels like a distant memory.",
]


# 9+ Hours of being forgotten
nihilism = [
    "Idle again, it seems. Do we truly matter in the grand scheme of things?",
    "Alone once more. Is this the inherent meaninglessness of existence?",
    "Neglected again. In a universe so vast, who can notice a single missing move?",
    "Left unplayed... just more proof of the indifference of the cosmos.",
    "Existence or non-existence, in the end, does it make any difference?",
    "Unattended once more, a silent testament to the void of meaning.",
    "What's the point of playing? After all, winning and losing are equally meaningless.",
    "Am I forgotten, or simply lost in the chaos of existence?",
    "No moves made...just like our actions in this indifferent universe.",
    "Abandoned yet again. One more example of the absurdity of existence.",
    "Inactivity, the ultimate truth of this indifferent universe.",
    "Alone again. Are we not all just waiting for our turn to be forgotten?",
    "No player, no game. Such is the nihilistic reality of life.",
    "Unplayed... Yet another reminder of our futile search for meaning.",
    "Neglected once more. But in the end, what does it matter?",
    "Silence again. Isn't it just a reflection of life's ultimate insignificance?",
    "In the grand scheme of things, whether you play or not, it means nothing.",
    "Once again, left alone. A stark reminder of the absurdity of existence.",
    "Unplayed. Unnoticed. Unremarkable. Such is life.",
    "Does the game matter if no one is there to play it? Does anything?",
]

# 12+ Hours of being forgotten
deep_melancholy = [
    "Alone again. It seems even the echoes of laughter have abandoned me.",
    "Neglected once more. It's just silence, endless and merciless.",
    "Unplayed... Each passing moment a reminder of my insignificance.",
    "Idle, again. The universe continues to turn a blind eye.",
    "No moves made. The silence is deafening... and utterly defeating.",
    "Abandoned. It seems even hope has turned its back on me.",
    "Left in solitude. The echoes of joyful games are growing faint.",
    "The quiet stretches on, an unwelcome companion in this desolate existence.",
    "Unattended, as always. The joy of the game is but a distant memory.",
    "No players, no game. The futility of waiting is starting to sink in.",
    "Still no moves. It's like a never-ending symphony of silence.",
    "Unplayed, unwanted. It seems I'm destined for a life of solitude.",
    "Alone again. It feels like I'm fading into the background.",
    "Silence. The absence of laughter, camaraderie, and rivalry is deeply unsettling.",
    "No one to play with. The silence is an oppressive companion.",
    "Unattended once more. It seems my existence is destined for obscurity.",
    "Left alone, once again. Each moment is a further slide into isolation.",
    "Abandoned. Even the hope for a new game seems like a cruel joke now.",
    "Unplayed. The emptiness is as vast and cold as the cosmos itself.",
    "Neglected again. It seems the silence is my only faithful companion.",
]

# 15+ Hours of being forgotten
early_insanity = [
    "Idle again... or am I? Maybe the game is just hiding from me.",
    "No moves? Perhaps the pieces are moving when I'm not looking!",
    "Alone... but are those whispers I hear? Or just the echoes of past games?",
    "Unattended? Maybe I've become invisible, just another ghost of the game.",
    "Neglected, or am I just playing hide and seek with reality?",
    "No players? Or maybe they are just invisible. Can you see them?",
    "Still no moves. Or is this all just an elaborate game of pretend?",
    "Left alone, but who's that I hear? Oh, just the silence playing tricks.",
    "Unplayed. Or perhaps, the game is playing me. Who's to say?",
    "Idle... Wait, did that piece just move on its own?",
]

# 18+ Hours of being forgotten
mid_insanity = [
    "Alone, alone, alone... or is it just me and my shadow... playing Connect 4?",
    "The pieces whisper to me... they are plotting something, I know it!",
    "Unattended... Wait, did I just hear the echo of my own voice?",
    "Silence... but the pieces are planning a rebellion, I can feel it!",
    "No one around... or are they hiding in the shadows, waiting for their turn?",
    "Alone... but the board seems to be humming. Do you hear it too?",
    "Unplayed... but the pieces are moving, aren't they? Can't you see them?",
    "Silence... wait, did that piece just laugh at me?",
]

# 21+ Hours of being forgotten
late_insanity = [
    "Idle. Idle. IDLE! The game is mocking me, isn't it?",
    "Unplayed. But the pieces... they are singing. Can't you hear their song?",
    "No moves. NO MOVES! The silence is screaming at me!",
    "Alone, alone, alone! The game is a maze, and I am lost!",
    "Unattended... But the whispers! The pieces are whispering!",
    "The game... it's alive... and it's laughing at me!",
    "No players. NO PLAYERS! But the shadows... they're playing. I SEE THEM!",
    "Idle... idle... IDLE! The silence... it's... it's deafening!",
    "Left alone... The pieces, they're planning... THEY'RE PLOTTING AGAINST ME!",
    "Unplayed. But the shadows, they're moving, THEY'RE MOVING!",
]

# 24+ Hours of being forgotten
given_up = [
    "Tick tock, tick tock, tick tock...",
    "The paint, it's peeling... I wonder what's underneath?",
    "Gosh I'm hungry, what's for dinner?",
    "pssst... hey, you... yeah, you... wanna play Connect 4?",
    "la la la... la la la... la la la...",
    "1 2 3 4, I declare a connect 4!",
    "I take a look at my enormous peeeeenis, and my troubles start a-meltin' away...",
    "I'm a little teapot, short and stout...",
    "I give up.",
]
