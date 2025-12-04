"""Simple Secret Santa Bot using Telegram Bot API"""
import telebot

from dataclasses import dataclass
import random

from messages import Language, MessageSanta, MessageSantaSucks
from model import SecretSantaModel, User


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
model = SecretSantaModel()

@bot.message_handler(commands=['start'])
def start(message):
    """Handles the /start command"""

    chat_id = message.chat.id
    
    if message.chat.type in ("supergroup", "channel", "group"):
        bot.send_message(chat_id, MessageSanta.GROUP_CHAT_NOTICE)

    else:
        newUser = User(chat_id=chat_id, name=message.from_user.first_name)

        model.add_user(newUser)
        bot.send_message(chat_id, MessageSanta.WELCOME.format(newUser.name))

@bot.message_handler(commands=['santa_sucks'])
def santa_sucks(message):
    """Handles the /santa_sucks command"""
    chat_id = message.chat.id

    if not model.has_user(chat_id):
        bot.send_message(chat_id, "Спочатку виконайте /start")
        return

    user = model.get_user(chat_id)
    user.language_code = Language.SANTA_SUCKS
    bot.send_message(chat_id, "Ви успішно переключилися на режим Таємного Друга, а не цих ваших стрьомних дідів!")

@bot.message_handler(commands=['name'])
def change_name(message):
    """Handles the /name command"""
    chat_id = message.chat.id
    args = message.text.split(" ")

    if len(args) < 2:
        bot.send_message(chat_id, "Будь ласка, вкажіть нове ім'я після команди /name")
        return

    new_name = " ".join(args[1:])

    if not model.has_user(chat_id):
        bot.send_message(chat_id, "Спочатку виконайте /start")
        return

    model.change_name(chat_id, new_name)
    bot.send_message(chat_id, f"Ваше ім'я було змінено на {new_name}")

@bot.message_handler(commands=['participants'])
def participants(message):
    """Handles the /participants command"""

    msg = "Учасники гри:\n"
    registered_users = [user for user in model.users.values() if user.registered]
    for user_name in model.get_registered_user_names():
        msg += "\n- " + user_name
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['register'])
def register(message):
    """Handles the /register command"""
    chat_id = message.chat.id

    if not model.has_user(chat_id):
        bot.send_message(chat_id, "Спочатку виконайте /start")
        return

    user = model.get_user(chat_id)
    user.registered = True
    bot.send_message(chat_id, f"{user.name}, ви успішно зареєстровані в грі Таємний Санта!")

@bot.message_handler(commands=['assign'])
def assign(message):
    """Handles the /assign command"""
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "Команду /assign можна виконувати лише в чаті.")
        return

    bot.send_message(message.chat.id, "Починаю розподіл Сант/друзів...")

    santa_mappings = model.assign_santas()

    for mapping in santa_mappings:
        giver: User = mapping.giver
        receiver: User = mapping.receiver

        if giver.language_code == Language.SANTA_SUCKS:
            bot.send_message(giver.chat_id, MessageSantaSucks.ASSIGNMENT.format(giver.name, receiver.name))
        else:
            bot.send_message(giver.chat_id, MessageSanta.ASSIGNMENT.format(giver.name, receiver.name))

    bot.send_message(message.chat.id, "Розподіл Санта завершено і повідомлення надіслано всім учасникам!")
    generate_result_file(santa_mappings)


def generate_result_file(santa_mappings: list) -> str:
    """Generates a text file with the Santa assignments and returns the file path"""

    file_path = "secret_results.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        for mapping in santa_mappings:
            giver: User = mapping.giver
            receiver: User = mapping.receiver
            file.write(f"{giver.name} -> {receiver.name}\n")
    return file_path


# Start polling
bot.infinity_polling()



    
