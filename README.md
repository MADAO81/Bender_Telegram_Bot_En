# 🤖 Bender Telegram Bot

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)

**Bender Bending Rodriguez** from *Futurama* is now living in your Telegram chat. He roasts, comments on images, interrupts conversations on a whim, changes mood based on time of day, and reacts to trigger words.

> *"Bite my shiny metal ass!"* — Bender

---

## 📋 Features

| Feature | Description |
| :--- | :--- |
| 💬 **Comments on messages** | 20% chance to interrupt any conversation |
| 🎯 **Trigger words** | Instantly reacts to «beer», «work», «Fry» and others |
| 🎭 **Mood system** | Changes personality based on time of day |
| 📊 **Statistics** | Tracks jokes and user interactions |
| 🖼️ **Image comments** | Analyzes photos via OpenAI Vision |
| 🧠 **OpenAI integration** | Generates smart replies in Bender's style |
| ⏰ **Working hours** | Active weekdays, 9:00–23:00 |
| 🔒 **Secure token storage** | All secrets in `.env` file |

---

## 🎯 Trigger Words

Bender instantly reacts to these words:

| Word | Reaction |
| :--- | :--- |
| **beer, whiskey** | 🍺 Gets excited, demands a drink |
| **work, boss** | 😠 Gets angry, curses |
| **Fry** | 🤖 Nostalgic, calls him a friend |
| **Zoidberg** | 🦑 Disgusted |
| **Leela** | 👁️ Respectful and slightly scared |
| **vacation, weekend** | 😌 Happy |

---

## 🤖 Bot Commands

| Command | What it does |
| :--- | :--- |
| `/start` | Greeting with current mood |
| `/stats` | Weekly joke statistics |
| `/mood` | Current Bender mood |
| `/characters` | Thoughts on Futurama characters |
| `/help` | Command and trigger reference |

---

## 📁 Project Structure

```text
bender_telegram_bot_en/
├── bender_bot.py              # Main bot code
├── jokes/                     # Modules
│   ├── __init__.py
│   ├── jokes_bank.py          # Joke bank (1000+)
│   ├── mood_system.py         # Mood system
│   ├── mood_templates.py      # Joke generator
│   └── triggers.py            # Trigger words
├── stats.json                 # Statistics (auto-generated)
├── .env                       # Tokens (DO NOT COMMIT!)
├── .env.example               # Token template
├── requirements.txt           # Dependencies
├── .gitignore                 # Ignores .env and cache
└── README.md                  # This file
🚀 Quick Start
1. Clone the repository
bash
git clone https://github.com/MADAO81/Bender_Telegram_Bot_En.git
cd bender-telegram-bot-en
2. Install dependencies
bash
pip install -r requirements.txt
3. Get your tokens
What	Where to get
TELEGRAM_TOKEN	From @BotFather on Telegram
OPENAI_API_KEY	From your OpenAI Platform dashboard
4. Configure environment
Create a .env file in the project root:

env
TELEGRAM_TOKEN=your_bot_token
OPENAI_API_KEY=sk-proj-your_openai_key
5. Run the bot
bash
python bender_bot.py
⚙️ Configuration
All settings are at the top of bender_bot.py:

Parameter	Default	Description
WEEKLY_JOKE_LIMIT	20	Maximum jokes per week
CHANCE_TO_JOKE	0.20	20% chance to joke per message
COOLDOWN_MINUTES	15	Minutes between jokes
WORK_HOURS_START	9	Start of working day
WORK_HOURS_END	23	End of working day
☁️ Deployment Options
Option 1: Render.com (Free tier)
Push your code to GitHub

Go to render.com → New → Background Worker

Connect your repository

Add environment variables:

TELEGRAM_TOKEN

OPENAI_API_KEY

Set Build Command: pip install -r requirements.txt

Set Start Command: python bender_bot.py

Click Create Worker

Option 2: Fly.io
bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch --name bender-bot
fly secrets set TELEGRAM_TOKEN=your_token
fly secrets set OPENAI_API_KEY=your_key
fly deploy
Option 3: Railway.app
Go to railway.app

Click New Project → Deploy from GitHub

Select your repository

Add environment variables in the dashboard

Railway auto-deploys on push

Option 4: Heroku
bash
heroku create bender-bot
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
🧪 Example Interactions
User:
— Beer?

Bender:

— 🍺 Beer! Where?! I can smell it! Pour me one!

User:
— Work is killing me.

Bender:

— 😠 Work? Ugh! Don't say that word — it causes corrosion.

User:
— @BenderBot hey!

Bender:

— 🤖 Hey meatbag! Bite my shiny metal ass!

❓ FAQ
How do I disable OpenAI?
Comment out OPENAI_API_KEY in .env.

How do I change joke frequency?
Change CHANCE_TO_JOKE = 0.20 in bender_bot.py.

Where is statistics stored?
In stats.json in the project root.

How do I update the bot on the server?

bash
git pull origin main
systemctl restart benderbot   # if using systemd
🛠️ Tech Stack
Python 3.9+

python-telegram-bot

OpenAI API

python-dotenv

📄 License
MIT — free to use, modify, and distribute.

👤 Author
MADAO81 — development, server setup, Telegram and OpenAI integration.

Made with love (and hatred for humanity) for the Telegram community.

🤝 Contributing
Found a bug or have an idea? Open an Issue or Pull Request. Bender would approve (probably not, but give it a shot).

Bite my shiny metal ass! 🍺🤖
