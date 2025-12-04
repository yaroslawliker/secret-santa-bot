"""Simple Secret Santa Bot using Telegram Bot API"""
import telebot

from dataclasses import dataclass
import random

from messages import Language, MessageSanta, MessageSantaSucks
from model import User


def read_token() -> str:
    """Reads token from the token.txt file in the root"""
    token = ""
    with open("./token.txt", "rt") as file:
        token = file.read()
    return token
   
        

# Initialize bot
TOKEN = read_token()
bot = telebot.TeleBot(TOKEN)

# In-memory storage for users
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    """Handles the /start command"""

    chat_id = message.chat.id
    
    if message.chat.type == "group":
        bot.send_message(chat_id, "Так-так, бачу це груповий чат. Можете написати /participants щоби отримати список тих хто вже зареєструвався.")

    else:
        newUser = User(chat_id=chat_id, first_name=message.name)

        users[chat_id] = newUser
        bot.send_message(chat_id, MessageSanta.WELCOME.format(newUser.name))

@bot.message_handler(commands=['register'])
def register(message):
    """Handles the /register command"""
    chat_id = message.chat.id

    if chat_id not in users:
        bot.send_message(chat_id, "Спочатку виконайте /start")
        return

    user = users[chat_id]
    bot.send_message(chat_id, f"{user.name}, ви успішно зареєстровані в грі Таємний Санта!")



    
