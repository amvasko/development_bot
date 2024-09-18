import telebot, os
from telebot import types
from data.data import hello_users,info_dovidka,main_question,chatbotIsImportant
from dotenv import load_dotenv

# Load env variables
load_dotenv();
# Створюємо бота з токеном
bot = telebot.TeleBot("7132175351:AAFYrbdtinfM2cl_-mWpZqlKovNQsqySHyk")

@bot.message_handler(commands=['start'])
def start(message):
    # Пропонуємо користувачу підписатися
    bot.send_message(message.chat.id,hello_users);
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Підписатися на бота", callback_data="subscribe")
    btn2 = types.InlineKeyboardButton("Ні, дякую", callback_data="no_thanks")
    markup.add(btn1, btn2)  # Ви можете додати обидві кнопки одночасно
    bot.send_message(message.chat.id, "Ви підписались на чат-бот. Чи бажаєте отримувати сповіщення?", reply_markup=markup)
# Обробник натискань кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "subscribe":
        # Відправляємо прохання поділитися номером телефону
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button_phone = types.KeyboardButton(text="Поділитися номером телефону", request_contact=True)
        markup.add(button_phone)
        bot.send_message(call.message.chat.id, "Будь ласка, надішліть свій номер телефону.", reply_markup=markup)
    elif call.data == "info":
        bot.send_message(call.message.chat.id,info_dovidka);

    elif call.data == "no_thanks":
        # Викликати меню після вибору "Ні, дякую"
        show_menu(call.message.chat.id)

# Отримання номера телефону
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    if message.contact is not None:
        # Відправляємо код підтвердження
        bot.send_message(message.chat.id, "На ваш номер надіслано код підтвердження. Введіть його:")
        # Додаємо логіку для генерації і відправлення коду
        # Введення коду підтвердження і перевірка може бути реалізована тут.

# Функція для показу меню користувачу
def show_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Отримати інформаційну довідку", callback_data="info")
    button2 = types.InlineKeyboardButton(main_question, callback_data="question")
    button3 = types.InlineKeyboardButton(chatbotIsImportant, callback_data="form")
    markup.add(button1, button2, button3)
    bot.send_message(chat_id, "Оберіть доступну дію:", reply_markup=markup)

# Основний цикл
bot.polling(none_stop=True)