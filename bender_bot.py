# bender_bot.py — English version with OpenAI ready
import os
import sys
import json
import random
import asyncio
from datetime import datetime, time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

from jokes.mood_system import get_joke_by_mood, get_mood_description
from jokes.jokes_bank import JOKES_BANK
from jokes.mood_templates import get_joke_with_generator
from jokes.triggers import get_trigger_reaction_with_mood

# ========== CONFIGURATION ==========
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN not found in .env!", file=sys.stderr)
    sys.exit(1)

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not found. AI features will be disabled.", file=sys.stderr)

WEEKLY_JOKE_LIMIT = 20
CHANCE_TO_JOKE = 0.20
COOLDOWN_MINUTES = 15
USE_OPENAI = bool(OPENAI_API_KEY)
STATS_FILE = 'stats.json'

WORK_HOURS_START = 9
WORK_HOURS_END = 23

TRIGGER_WORDS = ['beer', 'whiskey', 'work', 'boss', 'fry', 'leela', 'zoidberg', 'vacation', 'weekend']

# ========== WORKING HOURS ==========
def is_working_hours() -> bool:
    now = datetime.now()
    if now.weekday() in [5, 6]:
        return False
    current_time = now.time()
    start = time(WORK_HOURS_START, 0)
    end = time(WORK_HOURS_END, 0)
    return start <= current_time <= end

# ========== STATISTICS ==========
def load_stats() -> dict:
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'week_start': datetime.now().strftime('%Y-%m-%d'),
            'jokes_count': 0,
            'last_joke_time': None,
            'total_jokes': 0,
            'mood_stats': {},
            'users_interacted': []
        }

def save_stats(stats: dict):
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error saving stats: {e}", file=sys.stderr)

def can_joke(stats: dict) -> bool:
    week_start = datetime.strptime(stats['week_start'], '%Y-%m-%d').date()
    today = datetime.now().date()
    
    if (today - week_start).days >= 7:
        stats['week_start'] = today.strftime('%Y-%m-%d')
        stats['jokes_count'] = 0
        save_stats(stats)
    
    if stats['jokes_count'] >= WEEKLY_JOKE_LIMIT:
        return False
    
    if stats['last_joke_time']:
        last_joke = datetime.fromisoformat(stats['last_joke_time'])
        if (datetime.now() - last_joke).total_seconds() < COOLDOWN_MINUTES * 60:
            return False
    
    return True

def register_joke(stats: dict, mood=None):
    stats['jokes_count'] += 1
    stats['total_jokes'] = stats.get('total_jokes', 0) + 1
    stats['last_joke_time'] = datetime.now().isoformat()
    
    if mood:
        mood_name = mood.value if hasattr(mood, 'value') else str(mood)
        if 'mood_stats' not in stats:
            stats['mood_stats'] = {}
        stats['mood_stats'][mood_name] = stats['mood_stats'].get(mood_name, 0) + 1
    
    save_stats(stats)

def register_user(stats: dict, user_id: int, username: str = None):
    if 'users_interacted' not in stats:
        stats['users_interacted'] = []
    
    user_data = {
        'id': user_id,
        'username': username,
        'last_active': datetime.now().isoformat()
    }
    
    for i, user in enumerate(stats['users_interacted']):
        if user['id'] == user_id:
            stats['users_interacted'][i]['last_active'] = datetime.now().isoformat()
            if username:
                stats['users_interacted'][i]['username'] = username
            save_stats(stats)
            return
    
    stats['users_interacted'].append(user_data)
    save_stats(stats)

# ========== OPENAI HELPERS ==========
async def analyze_image(image_url: str) -> str:
    if not USE_OPENAI:
        return "🧠 OpenAI is disabled. But nice picture, I guess!"
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": 
                    "You are Bender Bending Rodriguez from Futurama. "
                    "You are a selfish, cynical, drinking robot. "
                    "Comment on this image briefly, sarcastically, in your signature style. "
                    "If there's a person — roast them. If there's food — ask where yours is."
                },
                {"role": "user", "content": [
                    {"type": "text", "text": "Comment on this image as Bender:"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_tokens=150,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Vision API error: {e}", file=sys.stderr)
        return "🤖 This picture is garbage, I've seen better. Bring me whiskey!"

async def get_openai_response(prompt: str) -> str:
    if not USE_OPENAI:
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": 
                    "You are Bender Bending Rodriguez from Futurama. "
                    "You are a selfish, cynical, drinking robot. "
                    "Reply briefly, rudely, sarcastically. "
                    "You're the best, everyone else is garbage. "
                    "Use Bender's signature phrases: 'Bite my shiny metal ass!', 'Kill all humans!', 'Hey meatbag!'."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI error: {e}", file=sys.stderr)
        return None

# ========== BOT COMMANDS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    mood_joke, current_mood = get_joke_by_mood()
    mood_desc = get_mood_description(current_mood)
    
    await update.message.reply_text(
        f"🤖 *Bender Bending Rodriguez* — at your service!\n\n"
        f"My current mood: {mood_desc}\n"
        f"Joke bank: {len(JOKES_BANK)}+ options\n"
        f"Weekly joke limit: {WEEKLY_JOKE_LIMIT}\n"
        f"Total jokes told: {stats.get('total_jokes', 0)}\n"
        f"{'🧠 OpenAI: ENABLED' if USE_OPENAI else '🧠 OpenAI: DISABLED'}\n"
        f"🎲 Joke chance: {int(CHANCE_TO_JOKE * 100)}%\n\n"
        f"*Bite my shiny metal ass!*\n\n"
        f"📝 *Commands:*\n"
        f"/stats — joke statistics\n"
        f"/mood — current mood\n"
        f"/characters — Futurama characters\n"
        f"/help — help",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    week_start = datetime.strptime(stats['week_start'], '%Y-%m-%d').date()
    days_left = 7 - (datetime.now().date() - week_start).days
    remaining = WEEKLY_JOKE_LIMIT - stats['jokes_count']
    
    mood_stats = stats.get('mood_stats', {})
    mood_report = "\n".join([f"  - {mood}: {count} jokes" for mood, count in mood_stats.items()]) if mood_stats else "  - no data yet"
    
    await update.message.reply_text(
        f"📊 *Bender's Statistics*\n\n"
        f"Jokes this week: {stats['jokes_count']}/{WEEKLY_JOKE_LIMIT}\n"
        f"Remaining: {remaining}\n"
        f"Days until reset: {days_left}\n"
        f"Total jokes ever: {stats.get('total_jokes', 0)}\n"
        f"Users served: {len(stats.get('users_interacted', []))}\n\n"
        f"*Mood distribution:*\n{mood_report}",
        parse_mode='Markdown'
    )

async def mood_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    _, current_mood = get_joke_by_mood()
    mood_desc = get_mood_description(current_mood)
    
    mood_tips = {
        "aggressive": "Don't make me angrier. Actually, do — I don't care. 🤬",
        "drunk": "It's time to bring me whiskey. 🥃",
        "sarcastic": "Your jokes are so 2015. Upgrade yourself. 😏",
        "philosophical": "Life is pain. Especially when you're meat. 🧐",
        "lazy": "Don't expect any heroics from me. I'm lying down. 😴",
        "happy": "I'm in a good mood today. Don't relax. 😊"
    }
    tip = mood_tips.get(current_mood.value, "Ask questions — maybe I'll answer.")
    
    await update.message.reply_text(
        f"🎭 *My current mood:*\n{mood_desc}\n\n"
        f"💡 *Tip:* {tip}\n\n"
        f"*Come at different times — my mood changes!*",
        parse_mode='Markdown'
    )

async def characters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    await update.message.reply_text(
        f"📺 *My take on Futurama characters:*\n\n"
        f"🤖 *Fry* — best friend. Idiot, but mine. Sometimes useful — brings beer.\n\n"
        f"🦑 *Zoidberg* — UGH! Slimy, disgusting, useless. Can't stand him.\n\n"
        f"👁️ *Leela* — respect. She could dismantle me. Better not mess with her.\n\n"
        f"👴 *Professor Farnsworth* — old weirdo. Created me, keeps forgetting to turn me off.\n\n"
        f"💰 *Amy Wong* — rich, but boring. I'd borrow money from her, but too lazy.\n\n"
        f"🐶 *Fry's dog* — Seymour... Let's not talk about it.\n\n"
        f"*Bite my shiny metal ass!*",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🤖 *Bender's Commands:*\n\n"
        f"/start — greeting and status\n"
        f"/stats — joke statistics\n"
        f"/mood — current mood\n"
        f"/characters — Futurama characters\n"
        f"/help — this help\n\n"
        f"*Trigger words:*\n"
        f"«work», «boss» — I get angry 😠\n"
        f"«beer», «whiskey», «vacation» — I get happy 🍺\n"
        f"«Fry», «Leela», «Zoidberg» — I talk about them\n\n"
        f"*Extra:*\n"
        f"🖼️ Send an image — I'll roast it\n"
        f"⏰ Working hours: 9:00–23:00 on weekdays\n"
        f"🎲 Random joke chance: {int(CHANCE_TO_JOKE * 100)}%\n"
        f"📊 Weekly joke limit: {WEEKLY_JOKE_LIMIT}\n"
        f"{'🧠 OpenAI: enabled' if USE_OPENAI else '🧠 OpenAI: disabled'}",
        parse_mode='Markdown'
    )

# ========== MESSAGE HANDLERS ==========
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    if not is_working_hours():
        await update.message.reply_text("⏰ I'm off duty. Come back weekdays, 9am–11pm.")
        return
    
    if update.message.chat.type in ['group', 'supergroup']:
        if not context.bot.username in update.message.caption:
            print("📨 Photo in group, not mentioned — ignoring", file=sys.stderr)
            return
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file.file_path}"
    
    await update.message.reply_text("🔍 Taking a look with my bulb-eyes...")
    comment = await analyze_image(image_url)
    await update.message.reply_text(f"🤖 *Bender:* {comment}", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == context.bot.id:
        return
    
    if not update.message.text:
        return
    
    if not is_working_hours():
        await update.message.reply_text("⏰ I'm off duty. Come back weekdays, 9am–11pm.")
        return
    
    text = update.message.text
    stats = load_stats()
    register_user(stats, update.effective_user.id, update.effective_user.username)
    
    is_mentioned = context.bot.username in text
    is_reply_to_bot = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    has_trigger = any(word in text.lower() for word in TRIGGER_WORDS)
    
    if is_mentioned or is_reply_to_bot:
        print(f"📨 Mentioned! Replying to: {text}", file=sys.stderr)
        _, current_mood = get_joke_by_mood()
        trigger_response = get_trigger_reaction_with_mood(text, current_mood)
        if trigger_response:
            await update.message.reply_text(f"🤖 *Bender:* {trigger_response}", parse_mode='Markdown')
            return
        
        await update.message.reply_text(
            f"🤖 *Bender:* {text}\n\n*Bite my shiny metal ass!*",
            parse_mode='Markdown'
        )
        return
    
    if has_trigger:
        print(f"📨 Trigger word detected: {text}", file=sys.stderr)
        _, current_mood = get_joke_by_mood()
        trigger_response = get_trigger_reaction_with_mood(text, current_mood)
        if trigger_response:
            await update.message.reply_text(f"🤖 *Bender:* {trigger_response}", parse_mode='Markdown')
        return
    
    if random.random() < CHANCE_TO_JOKE and can_joke(stats):
        print(f"📨 Bender decided to joke: {text}", file=sys.stderr)
        joke, current_mood = get_joke_by_mood()
        if random.random() < 0.3:
            joke = get_joke_with_generator(JOKES_BANK, use_generator_probability=0.3)
        register_joke(stats, current_mood)
        await update.message.reply_text(f"🤖 *Bender:* {joke}", parse_mode='Markdown')
        return
    
    if USE_OPENAI and len(text) > 10:
        print("🧠 Querying OpenAI...", file=sys.stderr)
        gpt_response = await get_openai_response(text)
        if gpt_response:
            await update.message.reply_text(f"🤖 *Bender:* {gpt_response}", parse_mode='Markdown')
            return
    
    print(f"📨 Bender stays silent: {text}", file=sys.stderr)

# ========== RUN ==========
if __name__ == "__main__":
    print("🚀 Bender is starting on VPS via polling...")
    print(f"📋 Telegram token: {TELEGRAM_TOKEN[:10]}... (hidden)")
    print(f"📋 OpenAI: {'ENABLED' if USE_OPENAI else 'DISABLED'}")
    print(f"⏰ Working hours: {WORK_HOURS_START}:00 — {WORK_HOURS_END}:00 weekdays")
    print(f"🎲 Joke chance: {int(CHANCE_TO_JOKE * 100)}% per message")
    print(f"📊 Weekly joke limit: {WEEKLY_JOKE_LIMIT}")
    print(f"⏱️ Cooldown: {COOLDOWN_MINUTES} minutes")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("mood", mood_command))
    app.add_handler(CommandHandler("characters", characters_command))
    app.add_handler(CommandHandler("help", help_command))
    
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
