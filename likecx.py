#!/usr/bin/env python3
import sys
import subprocess
import time
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes

# Auto-install required packages
required_packages = ['python-telegram-bot', 'requests']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"⚙️ Installing required package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Bot Configuration
TOKEN = "8203551425:AAGZO0fNW4T59Aq_iTLBREi8mDQAROhtm14"
API_KEY = "CHANDAN123"
WELCOME_IMAGE = "https://i.postimg.cc/dDMsbs3k/kmc-20250722-035435.png"
SUCCESS_IMAGE = "https://i.postimg.cc/8c7s8Xb3/1753324228554.png"
FAIL_IMAGE = "https://i.postimg.cc/3JDWn6N0/1753324417090.png"

EMOJI = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "like": "❤️",
    "player": "👤",
    "id": "🆔",
    "region": "🌐",
    "clock": "⏱️",
    "loading": "⏳",
    "celebrate": "🎉",
    "robot": "🤖",
    "handshake": "🤝"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['handshake']} SUBSCRIBE", url="https://t.me/+YSdNJcjdhUJjMGE9"),
            InlineKeyboardButton(f"{EMOJI['handshake']} JOIN CHANNEL", url="https://t.me/+YSdNJcjdhUJjMGE9")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"{EMOJI['robot']} <b>FREE FIRE LIKE BOT</b> {EMOJI['robot']}\n\n"
        f"{EMOJI['info']} <i>Hello {user.mention_html()}!</i>\n\n"
        f"{EMOJI['like']} I can send likes to any Free Fire player instantly!\n\n"
        f"{EMOJI['info']} <b>How to use:</b>\n"
        f"<code>/like ind UID</code>\n\n"
        f"{EMOJI['info']} <b>Example:</b>\n"
        f"<code>/like ind 2476897412</code>"
    )

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# /like command
async def like_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            f"{EMOJI['error']} <b>INVALID FORMAT</b>\n"
            f"{EMOJI['info']} Use: <code>/like ind UID</code>",
            parse_mode='HTML'
        )
        return

    region, uid = context.args[0].lower(), context.args[1]

    if region != "ind":
        await update.message.reply_text(
            f"{EMOJI['error']} <b>REGION NOT SUPPORTED</b>\n"
            f"{EMOJI['info']} Only 'ind' region is allowed.",
            parse_mode='HTML'
        )
        return

    processing_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Processing your request...</b>",
        parse_mode='HTML'
    )
    await asyncio.sleep(3)

    try:
        response = requests.get(
            f"https://officialfreefiremaxlikes.vercel.app/like?server_name={region}&uid={uid}&key={API_KEY}",
            timeout=10
        )
        data = response.json()

        if data.get("status") == 1 and data.get("LikesGivenByAPI", 0) > 0:
            caption = (
                f"{EMOJI['celebrate']} <b>LIKE SENT SUCCESSFULLY!</b>\n\n"
                f"{EMOJI['player']} <b>PLAYER:</b> {data['PlayerNickname']}\n"
                f"{EMOJI['id']} <b>UID:</b> {uid}\n"
                f"{EMOJI['region']} <b>REGION:</b> {region.upper()}\n"
                f"🔼 <b>BEFORE:</b> {data['LikesbeforeCommand']}\n"
                f"🔽 <b>AFTER:</b> {data['LikesafterCommand']}\n"
                f"{EMOJI['like']} <b>LIKES SENT:</b> {data['LikesGivenByAPI']}"
            )
            image_url = SUCCESS_IMAGE
        else:
            caption = (
                f"{EMOJI['warning']} <b>FAILED TO SEND LIKE</b>\n\n"
                f"{EMOJI['player']} <b>PLAYER:</b> {data.get('PlayerNickname', 'N/A')}\n"
                f"{EMOJI['id']} <b>UID:</b> {uid}\n"
                f"{EMOJI['like']} <b>LIKES NOW:</b> {data.get('LikesafterCommand', 'N/A')}"
            )
            image_url = FAIL_IMAGE

        keyboard = [
            [InlineKeyboardButton(f"{EMOJI['handshake']} SUBSCRIBE", url="https://t.me/yourchannel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await processing_msg.edit_media(
            media=InputMediaPhoto(media=image_url, caption=caption, parse_mode='HTML')
        )
        await processing_msg.edit_reply_markup(reply_markup=reply_markup)

    except Exception as e:
        await processing_msg.edit_text(
            f"{EMOJI['error']} <b>ERROR</b>\n<i>{e}</i>",
            parse_mode='HTML'
        )

# Run bot
def main():
    print(f"{EMOJI['robot']} Starting bot...")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("like", like_command))

    print(f"{EMOJI['success']} Bot is running!")
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print(f"{EMOJI['info']} Bot stopped.")
    finally:
        loop.close()

if __name__ == "__main__":
    main()
