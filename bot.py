import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# Твой токен
TOKEN = '7544393183:AAFbLdQ8F1A4JKOZtFgs9P43WzblcBa0bJE'
bot = telebot.TeleBot(TOKEN)

def load_songs():
    with open("songs.json", "r", encoding="utf-8") as file:
        return json.load(file)["songs"]

# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎵 Список песен"), KeyboardButton("ℹ О боте"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для отображения песен с аккордами. Выбирай, что тебе нужно:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "🎵 Список песен")
def send_songs(message):
    songs = load_songs()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for song in songs:
        markup.add(KeyboardButton(song["title"]))
    markup.add(KeyboardButton("⬅ Назад"))
    bot.send_message(message.chat.id, "Выбери песню:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [song["title"] for song in load_songs()])
def send_song_text(message):
    songs = load_songs()
    for song in songs:
        if message.text == song["title"]:
            bot.send_message(message.chat.id, f"🎵 {song['title']}\n\n{song['text']}")

@bot.message_handler(func=lambda message: message.text == "ℹ О боте")
def about_bot(message):
    bot.send_message(message.chat.id, "Этот бот позволяет просматривать песни с аккордами. Используй кнопки для навигации!")

@bot.message_handler(func=lambda message: message.text == "⬅ Назад")
def back_to_main(message):
    bot.send_message(message.chat.id, "Возвращаюсь в главное меню:", reply_markup=main_menu())

# Обработчик для всех остальных сообщений, чтобы не вызывать ошибку
@bot.message_handler(func=lambda message: True)
def handle_unexpected_message(message):
    bot.send_message(message.chat.id, "Я не понял твоё сообщение. Пожалуйста, используй кнопки для навигации!")

bot.polling()
