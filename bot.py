import telebot
TOKEN = '1792859514:AAEoaxCh_xVkl7CO3bw1w2vJC12m39HDKbk'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_menu(message):
    """Выводит приветственное сообщение вместе со стартовым меню."""
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    welcome_msg = (f"Я бот для изучения новых слов английского языка начального уровня.\n"
                   f"Приятно познакомиться, {message.from_user.first_name}.")
    user_markup = InlineKeyboardMarkup(row_width=2)
    user_markup.add(InlineKeyboardButton('Помощь', callback_data='help'),
                    InlineKeyboardButton('Выбрать тему', callback_data='choose_topic'),
                    InlineKeyboardButton('Узнать слово', callback_data='get_random_word'),
                    InlineKeyboardButton('Пройти тест', callback_data='random_test'))
    bot.send_message(message.from_user.id, welcome_msg, reply_markup=user_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def get_help(call):
    """Выводит справку пользователя."""
    message = call.message
    bot.send_message(message.chat.id, text="Это справка.")  # вывести справку


@bot.callback_query_handler(func=lambda call: call.data == 'get_random_word')
def get_random_word(call):
    """Выводит случайное слово и его перевод."""
    message = call.message
    # подключиться к облачному хранилищу данных
    # получить случайное слово
    bot.send_message(message.chat.id, text="Это случайное слово.")  # отправить случайное слово


@bot.callback_query_handler(func=lambda call: call.data == 'random_test')
def random_test(call):
    """Позволяет пройти тест на знание 20 случайных слов."""
    message = call.message
    # подключиться к облачному хранилищу данных
    # получить 80 случайных слов
    # сделать викторину выбора перевода


@bot.callback_query_handler(func=lambda call: call.data == 'choose_topic')
def get_topic(call):
    """Открытие консоли выбора темы."""


@bot.callback_query_handler(func=lambda call: call.data == 'topic_menu')
def topic_menu(call):
    """Открытие консоли выбранной темы."""


@bot.callback_query_handler(func=lambda call: call.data == 'get_topic_word')
def get_topic_word(call):
    """Выводит случайное слово по теме и его перевод."""


@bot.callback_query_handler(func=lambda call: call.data == 'topic_test')
def topic_test(call):
    """Позволяет пройти тест на знание всех слов в теме."""


@bot.callback_query_handler(func=lambda call: call.data == 'words_in_topic')
def words_in_topic(call):
    """Выводит все слова в теме вместе с переводом."""


@bot.callback_query_handler(func=lambda call: call.data == 'test_case')
def test_case(call):
    """Выводит вопрос вида /слово_на_английском переводится на русский как../ с 4-мя вариантами ответа."""


bot.polling(none_stop=True)
