# jokes/mood_templates.py
# Joke generator from templates — infinite variety

import random

TEMPLATES = {
    "insult": [
        "Your mom is {0}",
        "You're so {0} that even {1}",
        "Your face looks like a {0}",
        "Your brain is the size of a {0}",
        "You're dumber than {0}",
        "Your logic is like {0}",
    ],
    "comparison": [
        "You're like {0}, only worse",
        "Even {0} is better than you",
        "You and {0} are the same thing",
        "The difference between you and {0} is that {0} is useful",
    ],
    "self_praise": [
        "I'm {0}% {1}",
        "My {0} is better than your {1}",
        "I have {0}, you have {1}",
    ],
    "random": [
        "You know, {0} is {1}. And you're {2}.",
        "If {0} were {1}, you'd be {2}.",
        "I'm not saying {0}, but {0}.",
    ]
}

INSULTS = [
    "stupid", "rusty", "old", "broken", "useless",
    "obsolete", "pointless", "pathetic", "lame", "worthless"
]

NOUNS = [
    "battery", "antenna", "gear", "wire", "chip",
    "processor", "transistor", "diode", "resistor", "capacitor"
]

COMPARISONS = [
    "Fry", "Zoidberg", "a broken toaster", "a calculator with dead batteries",
    "a robot vacuum", "an ATM with no money", "a traffic light"
]

def generate_random_joke():
    """Generates a random joke from templates"""
    template_type = random.choice(list(TEMPLATES.keys()))
    template = random.choice(TEMPLATES[template_type])

    if template_type == "insult":
        return template.format(random.choice(INSULTS), random.choice(NOUNS))
    elif template_type == "comparison":
        return template.format(random.choice(COMPARISONS))
    elif template_type == "self_praise":
        return template.format(random.randint(40, 99), random.choice(["titanium", "dolomite", "steel", "iron", "brass"]))
    else:
        return template.format(
            random.choice(["life", "love", "work", "money", "beer"]),
            random.choice(["painful", "funny", "stupid", "weird"]),
            random.choice(["Bender", "robot", "metal"])
        )

def get_joke_with_generator(static_jokes_list, use_generator_probability=0.3):
    """Returns either a static joke or a generated one (30% chance)"""
    if random.random() < use_generator_probability:
        return generate_random_joke()
    else:
        return random.choice(static_jokes_list)