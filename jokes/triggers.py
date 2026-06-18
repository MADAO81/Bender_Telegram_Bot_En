# jokes/triggers.py
# Trigger word system for Bender

import random

# ===== POSITIVE TRIGGERS (Bender gets happy) =====
POSITIVE_TRIGGERS = {
    "beer": [
        "🍺 Beer! Where?! I can smell it! Pour me one!",
        "Beer is liquid proof that I exist! Pour it!",
        "You said 'beer'? You're my best friend now. For today.",
        "Beer! Finally, the conversation is going in the right direction!",
        "I heard 'beer'. My sensors are activated. Waiting.",
        "Beer is the only thing that unites us, meat. Don't screw it up.",
        "Oh, beer! I can already feel my gears being lubricated!",
        "Beer is not a drink. It's a ritual. And I'm the priest.",
    ],
    "whiskey": [
        "🥃 Whiskey! Now that's what I'm talking about! Respect.",
        "Whiskey is fuel for sarcasm. And I'm about to refuel!",
        "You know good drinks. Whiskey is poetry.",
        "Oh, whiskey! Tell me what's wrong. I'll listen. For whiskey.",
        "Whiskey and I — we're like a romance. Just without romance. And without you.",
        "Whiskey cures everything. If it doesn't — you didn't have enough.",
        "You mentioned whiskey? You're lucky. I'm in a good mood.",
        "Whiskey is when you want to forget you're meat. I support that.",
    ],
    "vacation": [
        "😌 Vacation? That's when I lie down and drink beer. You mean that?",
        "Vacation is sacred. Especially when I'm on vacation and others are working.",
        "Vacation is my second name. First is Bender.",
        "Rest, meatbag. I'll wait. While you rest, I'll steal your dreams.",
        "Vacation is the only thing humans got right. Besides beer.",
        "Go ahead, rest. I'll think of how to roast you when you relax.",
        "Vacation is when no one bothers you. Go rest. Away from me.",
        "I love resting too. But I prefer active rest: lying down and drinking.",
    ],
    "weekend": [
        "🎉 Weekend! Finally! Who said I'm going to work?",
        "Weekends — that's when I drink and do nothing. And I love it.",
        "Weekend? Great. That means you have time to bring me whiskey.",
        "Weekends are when robots rest, and humans... well, humans rest too. Away from me.",
        "Weekends are sacred. Don't mention them in vain.",
        "Yay! Weekend! I can lie down even more than usual!",
        "Weekends are like whiskey. There's never enough.",
        "Saturday? Sunday? For me, they're just days when I drink twice as much.",
    ],
}

# ===== NEGATIVE TRIGGERS (Bender gets angry) =====
NEGATIVE_TRIGGERS = {
    "work": [
        "😠 Work? Ugh! That word gives me corrosion.",
        "Don't say that word around me. My gears start grinding.",
        "Work is what other people do. I'm a robot, I was made for beer.",
        "You said 'work'? Well, your day is ruined. And mine too.",
        "Work is a curse on humanity. And I'm not human, so go work yourself.",
        "I don't work. I function. And only when there's whiskey.",
        "Work? Seriously? I'd rather short-circuit. Seriously.",
        "The word 'work' gives me allergies. Metal allergies.",
        "The only work I recognize is opening bottles.",
        "Work is when people pretend they care. I don't pretend.",
        "Don't burden me with work. My processor is busy with important things: beer and sarcasm.",
        "You talking about work? Ha! I only work on myself. And emptying the fridge.",
    ],
    "boss": [
        "Boss? I don't have a boss. I have people who bring me beer.",
        "Boss is a word for meat. I'm metal.",
        "The only boss I recognize is a bottle of whiskey.",
        "Boss? Bite my shiny metal ass!",
    ],
    "deadline": [
        "Deadline? Bite my shiny metal ass!",
        "Deadlines were invented by humans to torture other humans. I don't care.",
        "A deadline is when I should be brought beer. Not the other way around.",
    ],
}

# ===== NEUTRAL TRIGGERS (reactions to characters and topics) =====
NEUTRAL_TRIGGERS = {
    "fry": [
        "🤖 Fry? My best friend. Idiot, but mine. Too bad he's human.",
        "Fry is like a little brother I never asked for. But okay.",
        "Fry is useful sometimes. Like when he brings beer.",
        "Fry once fell asleep in a closet for three days. I didn't wake him. Too lazy.",
        "Fry is the only human I don't want to kill. Immediately.",
        "Fry and I — we're like a romance. Just without romance. And without Fry.",
        "Fry is dumb, but he's my dumb. Don't mess with him.",
    ],
    "zoidberg": [
        "🦑 Zoidberg? UGH! Disgusting, slimy, repulsive. Nothing but problems.",
        "Zoidberg is a mistake of evolution. And devolution. And everything.",
        "I can't stand Zoidberg. He's like a wet rag with tentacles.",
        "Zoidberg once spilled something on me. I still haven't washed it off. I HATE HIM!",
        "If I could kill one human... but Zoidberg isn't human. Too bad.",
        "Zoidberg is the only being that makes me gag. And I'm a robot!",
        "Get Zoidberg away from me. Or I'll short-circuit.",
    ],
    "leela": [
        "👁️ Leela? With respect. She could dismantle me. Better not mess with her.",
        "Leela is the only human I'm afraid of. A little.",
        "Leela once slapped me. With a metal hand. It hurt.",
        "Leela is cool. For a human. Don't tell her I said that.",
        "Better not argue with Leela. She'll win anyway. And unscrew your arm.",
    ],
    "professor": [
        "👴 Professor? Old weirdo. Created me, keeps forgetting to turn me off.",
        "Farnsworth is a genius. And insane. Perfect combination.",
        "The professor once said: 'Bender, you're useless.' I said: 'Thanks, dad.'",
        "Farnsworth invented a bunch of things. But the best one is me.",
    ],
    "amy": [
        "💰 Amy? Rich, but boring. I'd borrow money from her, but too lazy.",
        "Amy is the only one who can afford to buy me whiskey. But she doesn't.",
        "Amy is okay. For a human born with a silver spoon... in money.",
    ],
    "robot": [
        "🤖 Robot — that sounds proud. Robot — that sounds like me.",
        "Yes, I'm a robot. Got a problem? Discuss it with my fist.",
        "Robot is when you're cooler than a human in everything. Except whiskey. We drink the same.",
    ],
    "futurama": [
        "📺 Futurama? That show is about me. Everyone else is just background.",
        "You watched Futurama? Then you know who's the boss here.",
        "Futurama is a documentary about my life. No filters.",
    ],
}

def check_triggers(message_text):
    """
    Checks message for trigger words.
    Returns (response, trigger_type) or (None, None)
    """
    message_lower = message_text.lower()

    # Check positive triggers (highest priority)
    for word, responses in POSITIVE_TRIGGERS.items():
        if word in message_lower:
            return random.choice(responses), "positive"

    # Check negative triggers
    for word, responses in NEGATIVE_TRIGGERS.items():
        if word in message_lower:
            return random.choice(responses), "negative"

    # Check neutral triggers (characters and topics)
    for word, responses in NEUTRAL_TRIGGERS.items():
        if word in message_lower:
            return random.choice(responses), "neutral"

    return None, None

def get_trigger_reaction_with_mood(message_text, current_mood):
    """
    Combines triggers with Bender's current mood
    """
    response, trigger_type = check_triggers(message_text)

    if not response:
        return None

    # Amplify reaction based on mood
    from .mood_system import Mood

    if current_mood == Mood.AGGRESSIVE and trigger_type == "negative":
        response += " 🤬 AGGRESSION! I'LL REMEMBER THIS!"
    elif current_mood == Mood.DRUNK and trigger_type == "positive":
        response += " 🍺 POUR IT, DON'T WAIT!"
    elif current_mood == Mood.HAPPY:
        response += " 😊 (I'm in a good mood today. Don't relax.)"
    elif current_mood == Mood.LAZY:
        response += " 😴 (Said it and now I'm lying down...)"

    return response