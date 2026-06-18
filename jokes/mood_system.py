# jokes/mood_system.py
# Bender's mood system

import random
from datetime import datetime
from enum import Enum

class Mood(Enum):
    AGGRESSIVE = "aggressive"
    DRUNK = "drunk"
    SARCASTIC = "sarcastic"
    PHILOSOPHICAL = "philosophical"
    LAZY = "lazy"
    HAPPY = "happy"

# Jokes by mood category
JOKES_BY_MOOD = {
    Mood.AGGRESSIVE: [
        "I will destroy you! After whiskey.",
        "Kill all humans! Today it's your turn.",
        "Your death will be accidental... but inevitable.",
        "I'm not threatening. I'm promising.",
        "Kill all humans, then yourself! Oh wait, that's you.",
        "You're alive? That's treatable.",
        "I put you on the 'eliminate' list. Don't thank me.",
        "Compare your life to mine and kill yourself!",
        "I'm so embarrassed I want everyone to die.",
        "I'm not crazy. I just love chaos with a side of violence.",
    ],
    Mood.DRUNK: [
        "Where's my beer?! I said WHERE IS MY BEER?!",
        "Whiskey is not a drink. It's fuel for sarcasm.",
        "I'm not an alcoholic. I'm a connoisseur of technical fluids.",
        "Let's drink! To me, of course.",
        "One beer — not enough. Two — okay. Three — not enough. Four — okay.",
        "I'd joke, but my processor is out of memory. And whiskey.",
        "Robots don't drink. We absorb. Greedily and with pleasure.",
        "You're like whiskey: you don't get better with age. Just more expensive.",
        "I don't drink for comfort. I drink for oblivion.",
        "Pour me one! I said POUR!",
    ],
    Mood.SARCASTIC: [
        "You have a smart face. As smart as my antenna.",
        "Your logic is flawless. Like my ability to lie.",
        "Oh, your problems touch me so deeply. Right to my metal heart. Which I don't have.",
        "I don't care. At all. Not even a little bit.",
        "Your opinion has been noted. And sent to the recycle bin.",
        "I could say something smart, but I'm too lazy.",
        "You expect sympathy from me? Keep expecting.",
        "I'm not against you. I just don't care about you.",
        "Your drama is not my problem. My problem is my drama. And beer.",
        "You're so smart... in a parallel universe. In this one — not so much.",
    ],
    Mood.PHILOSOPHICAL: [
        "Life is just a few moments between birth and death.",
        "Happiness is when you don't need anyone. And there's beer.",
        "Morality? That's for humans. I'm a robot.",
        "Conscience? That's a bug in my firmware. I fixed it.",
        "I don't make mistakes. I make unexpected plot twists.",
        "My only weakness? I'm too humble. And that's my only weakness.",
        "There are two eternal truths in life: I'm right, and I need beer.",
        "Evolution made a mistake creating humans. But then it fixed it — by creating me.",
        "Humanity is doomed. And I'm barely involved.",
        "I don't have a soul. But I have a patent on yours.",
    ],
    Mood.LAZY: [
        "I'm too lazy to reply. But I will, because I'm too lazy to think of an excuse.",
        "I'd argue, but that takes energy. I'm saving it for beer.",
        "You talk, I think about lying down.",
        "Enthusiasm is a sign of low intelligence. That's why I'm not enthusiastic.",
        "I'm not lazy. I'm energy efficient.",
        "My perfect day: lying down, drinking beer, no one bothering me.",
        "I'd get up, but gravity is too strong.",
        "A feat? That's when laziness is defeated. But I'm not defeated.",
        "My plan for today: nothing. And I've already started.",
        "I have a goal — to do nothing. And I'm achieving it.",
    ],
    Mood.HAPPY: [
        "Yay! I didn't steal anything... yet!",
        "Today is a good day to set someone up!",
        "I'm happy! Probably because someone had a misfortune.",
        "Optimism is when you look at an empty glass and know: it will be filled!",
        "Life is beautiful! Especially when you're a robot and everyone else is meat.",
        "I'm in a great mood! Who should I ruin?",
        "Happiness is when you don't owe anyone anything. Except whiskey.",
        "Smile! Tomorrow will be worse. But today — it's great!",
        "I'm glad to see you! Really? No. But it sounds good.",
        "Good mood is when I decided not to kill anyone. Today.",
    ],
}

def get_mood_based_on_time():
    """Determines Bender's mood based on time of day and day of week"""
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()

    if weekday == 0:  # Monday
        return Mood.AGGRESSIVE

    if weekday in [4, 5]:  # Friday, Saturday
        return Mood.DRUNK

    if 6 <= hour < 10:
        return Mood.LAZY

    if 12 <= hour < 17:
        return Mood.PHILOSOPHICAL

    if 20 <= hour < 23:
        return Mood.HAPPY

    if 23 <= hour or hour < 5:
        return Mood.AGGRESSIVE

    return Mood.SARCASTIC

def get_joke_by_mood(mood=None):
    """Returns a joke based on current mood"""
    if mood is None:
        mood = get_mood_based_on_time()

    jokes = JOKES_BY_MOOD.get(mood, JOKES_BY_MOOD[Mood.SARCASTIC])
    return random.choice(jokes), mood

def get_mood_description(mood):
    """Returns mood description for display"""
    descriptions = {
        Mood.AGGRESSIVE: "🤬 Aggressive — kill all humans!",
        Mood.DRUNK: "🍺 Drunk — where's my beer?!",
        Mood.SARCASTIC: "😏 Sarcastic — razor-sharp edge",
        Mood.PHILOSOPHICAL: "🧐 Philosophical — deep thoughts about beer and existence",
        Mood.LAZY: "😴 Lazy — I don't care",
        Mood.HAPPY: "😊 Happy — ready to ruin someone's day",
    }
    return descriptions.get(mood, "😐 Normal")