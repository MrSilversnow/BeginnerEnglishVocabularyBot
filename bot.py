import telebot
import analytical_functions as af
from sqlalchemy import create_engine
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from json import dumps, loads
from tabulate import tabulate
from datetime import datetime


my_engine = create_engine('mysql+pymysql://root:password@localhost:3306/bot')
TOKEN = '1792859514:AAEoaxCh_xVkl7CO3bw1w2vJC12m39HDKbk'
bot = telebot.TeleBot(TOKEN)
TEST_CASES = dict()  # словарь для тестов для каждого пользователя: 'uid': test.
MSG_TO_DEL = dict()  # словарь для должных быть удаленными сообщений для каждого чата.


def delete_message(message):
    """Удаяляет сообщение message."""
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id, message_id)
    pop_msg_to_del(chat_id, message_id)


def add_msg_to_del(uid, msg_id):
    """Добавляет сообщение в список необходимых к удалению."""
    uid = str(uid)
    if uid in MSG_TO_DEL:
        MSG_TO_DEL[uid].append(msg_id)
    else:
        MSG_TO_DEL[uid] = list((msg_id,))


def pop_msg_to_del(uid, msg_id):
    """Удаляет сообщение msg_id для конкретного пользователя uid."""
    uid = str(uid)
    if uid in MSG_TO_DEL:
        if msg_id in MSG_TO_DEL[uid]:
            MSG_TO_DEL[uid].remove(msg_id)


def clear_history(uid):
    """Удаляет все предыдущие сообщение бота, имеющиеся в данном сеансе для конкретного пользователя."""
    uid = str(uid)
    if uid in MSG_TO_DEL:
        for msg_id in MSG_TO_DEL[uid]:
            bot.delete_message(uid, msg_id)
        del MSG_TO_DEL[uid]


@bot.message_handler(commands=['start'])
def start_handler(message):
    """Отвечает на команду /start. Проверяет наличие пользователя в БД. Позволяет перейти в главное меню."""
    uid = message.from_user.id
    clear_history(uid)
    username = message.from_user.username
    af.add_user_if_not_exist(my_engine, uid, username)  # Добавляем пользователя в БД, если его там нет.
    welcome_msg = (f"Я бот для изучения новых слов английского языка начального уровня.\n"
                   f"Приятно познакомиться, {message.from_user.first_name}.")
    user_markup = InlineKeyboardMarkup()
    user_markup.add(InlineKeyboardButton('Начать работу', callback_data=dumps('start_menu')))
    this_msg_id = bot.send_message(message.from_user.id, welcome_msg, reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)
    delete_message(message)


@bot.callback_query_handler(func=lambda call: loads(call.data) == 'start_menu')
def start_menu(call):
    """Выводит приветственное сообщение вместе со стартовым меню."""
    message = call.message
    bot.answer_callback_query(call.id)
    delete_message(message)
    uid = str(message.chat.id)
    if uid in TEST_CASES:
        del TEST_CASES[uid]
    welcome_msg = (f"Вы в главном меню Learn English Vocabulary, {message.from_user.first_name}.\n"
                   f"Чего бы вам сейчас хотелось бы?")
    user_markup = InlineKeyboardMarkup(row_width=2)
    user_markup.add(InlineKeyboardButton('Помощь', callback_data=dumps('help')),
                    InlineKeyboardButton('Выбрать тему', callback_data=dumps(('choose_topic', 0))),
                    InlineKeyboardButton('Узнать слово', callback_data=dumps('random_word')),
                    InlineKeyboardButton('Пройти тест', callback_data=dumps(('random_test', 0))))
    this_msg_id = bot.send_message(uid, welcome_msg, reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data) == 'help')
def get_help(call):
    """Выводит справку пользователя."""
    message = call.message
    uid = message.chat.id
    bot.answer_callback_query(call.id)
    delete_message(message)
    help_msg = (f"Вас приветствует справка Learn English Vocabulary.\nЭтот бот позволяет изучать некоторую лексику нача"
                f"льного уровня из английского языка.\nЕсли вы находитесь в главном меню то нажатие на кнопку приводит "
                f"к следующему эфекту:\nПомощь - вызов справки по програме\nВыбрать тему - открытие консоли выбора темы"
                f"\nУзнать случайное слово - вывод случайного слова\nПройти тест - прохождение теста из 10 вопросов\n")
    user_markup = InlineKeyboardMarkup()
    user_markup.add(InlineKeyboardButton('Главное меню', callback_data=dumps('start_menu')))
    this_msg_id = bot.send_message(uid, help_msg, reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data) == 'random_word')
def random_word(call):
    """Выводит случайное слово и его перевод."""
    message = call.message
    uid = message.chat.id
    bot.answer_callback_query(call.id)
    delete_message(message)
    rw = af.get_random_word(my_engine, uid)
    user_markup = InlineKeyboardMarkup()
    user_markup.add(InlineKeyboardButton('Главное меню', callback_data=dumps('start_menu')))
    this_msg_id = bot.send_message(uid, text=f"На английском: {rw[0]}\nНа русском: {rw[1]}",
                                   reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'choose_topic')
def choose_topic(call):
    """Меню выбора темы. Красивое. С пагинацией."""
    message = call.message
    uid = call.message.chat.id
    bot.answer_callback_query(call.id)
    delete_message(message)
    topics = af.select_topic(my_engine)
    topics = tuple(topic[1] for topic in topics)
    choose_msg = "Выберите тему из списка:\n"
    buttons = list()
    # Сначала рассмотрим случай без пагинации.
    if len(topics) <= 5:
        user_markup = InlineKeyboardMarkup(row_width=len(topics))
        for tn in range(len(topics)):
            choose_msg += f"{tn}. {topics[tn]}\n"
            buttons.append(InlineKeyboardButton(f'{tn}', callback_data=dumps(('topic_menu', tn))))
    # Теперь рассмотрим случай с пагинацией.
    else:
        stf = loads(call.data)[1]  # Номер первой темы из списка тем в текущей пагинации
        # Небольшая страховка от выхода stf за пределы
        if stf < 0:
            stf = 0
        elif stf >= len(topics):
            stf = len(topics) - 1
        topics = topics[stf:]
        user_markup = InlineKeyboardMarkup(row_width=5)
        if stf == 0:
            """t0 t1 t2 t3 >"""
            for tn in range(4):
                choose_msg += f"{tn}. {topics[tn]}\n"
                buttons.append(InlineKeyboardButton(f'{tn}', callback_data=dumps(('topic_menu', tn))))
            buttons.append(InlineKeyboardButton('>', callback_data=dumps(('choose_topic', 4))))
        elif len(topics) <= 4:
            """< t t t t"""
            if stf == 4:
                buttons.append(InlineKeyboardButton('<', callback_data=dumps(('choose_topic', stf-4))))
            else:
                buttons.append(InlineKeyboardButton('<', callback_data=dumps(('choose_topic', stf - 3))))
            for tn in range(len(topics)):
                choose_msg += f"{stf+tn}. {topics[tn]}\n"
                buttons.append(InlineKeyboardButton(f'{stf+tn}', callback_data=dumps(('topic_menu', stf+tn))))
        else:
            """< t t t >"""
            if stf == 4:
                buttons.append(InlineKeyboardButton('<', callback_data=dumps(('choose_topic', stf - 4))))
            else:
                buttons.append(InlineKeyboardButton('<', callback_data=dumps(('choose_topic', stf - 3))))
            for tn in range(3):
                choose_msg += f"{stf+tn}. {topics[tn]}\n"
                buttons.append(InlineKeyboardButton(f'{stf+tn}', callback_data=dumps(('topic_menu', stf+tn))))
            buttons.append(InlineKeyboardButton('>', callback_data=dumps(('choose_topic', stf + 3))))
    user_markup.add(*buttons)
    user_markup.add(InlineKeyboardButton('Главное меню', callback_data=dumps('start_menu')))
    this_msg_id = bot.send_message(uid, choose_msg, reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'random_test')
def random_test(call):
    """Тест по всем словам на 10 вопросов с возможностью прервать его в любой момент."""
    message = call.message
    data = loads(call.data)
    uid = str(message.chat.id)
    qn = data[1]
    try:
        if qn == 0:
            TEST_CASES[uid] = af.get_random_test(my_engine, message.chat.id)
        else:
            is_correct = data[2]
            if is_correct:
                af.correct_answer(my_engine, uid, TEST_CASES[uid][qn-1][0][0])
                bot.answer_callback_query(call.id, 'Правильно!')
            else:
                 af.incorrect_answer(my_engine, uid, TEST_CASES[uid][qn-1][0][0])
                 bot.answer_callback_query(call.id, 'Неправильно!')
        if qn == len(TEST_CASES[uid]):  # если qn == "количество вопросов в тесте"
            start_menu(call)
        else:
            delete_message(message)
            question = f"Слово {TEST_CASES[uid][qn][0][0]} переводится на русский, как:"
            answers_markup = InlineKeyboardMarkup(row_width=2)
            buttons = list()
            for translation in TEST_CASES[uid][qn][1]:
                if translation == TEST_CASES[uid][qn][0][1]:
                    correct_answer = dumps(('random_test', qn + 1, True))
                    buttons.append(InlineKeyboardButton(translation, callback_data=correct_answer))
                else:
                    incorrect_answer = dumps(('random_test', qn + 1, False))
                    buttons.append(InlineKeyboardButton(translation, callback_data=incorrect_answer))
            answers_markup.add(buttons[0], buttons[1])
            answers_markup.add(buttons[2], buttons[3])
            answers_markup.add(InlineKeyboardButton('Главное меню', callback_data=dumps('start_menu')), row_width=1)
            this_msg_id = bot.send_message(message.chat.id, question, reply_markup=answers_markup).id
            add_msg_to_del(uid, this_msg_id)
    except KeyError:
        start_menu(call)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'topic_menu')
def topic_menu(call):
    """Меню темы."""
    data = loads(call.data)
    message = call.message
    delete_message(message)
    uid = call.message.chat.id
    tid = data[1] + 1
    topic_name = af.select_topic(my_engine, tid=tid)[0][1]
    m, n = af.get_topic_statistic(my_engine, uid, tid)
    topic_msg = f"Тема: {topic_name}\nИзученых слов: {m} из {n}"
    topic_markup = InlineKeyboardMarkup()
    topic_markup.add(InlineKeyboardButton('Случайное слово', callback_data=dumps(('topic_word', tid))),
                     InlineKeyboardButton('Тест по теме', callback_data=dumps(('topic_test', tid-1, 0))),
                     InlineKeyboardButton('Все слова в теме', callback_data=dumps(('topic_words', tid))))
    topic_markup.add(InlineKeyboardButton('Главное меню', callback_data=dumps('start_menu')))
    this_msg_id = bot.send_message(uid, topic_msg, reply_markup=topic_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'topic_test')
def topic_test(call):
    """Тест по всем словам темы с возможностью прервать его в любой момент."""
    message = call.message
    data = loads(call.data)
    uid = str(message.chat.id)
    qn = data[2]
    tid = data[1] + 1
    try:
        if qn == 0:
            TEST_CASES[uid] = af.get_topic_test(my_engine, tid)
        else:
            is_correct = data[3]
            if is_correct:
                af.correct_answer(my_engine, uid, TEST_CASES[uid][qn-1][0][0])
                bot.answer_callback_query(call.id, 'Правильно!')
            else:
                af.incorrect_answer(my_engine, uid, TEST_CASES[uid][qn-1][0][0])
                bot.answer_callback_query(call.id, 'Неправильно!')
        if qn == len(TEST_CASES[uid]):  # если qn == "количество вопросов в тесте"
            topic_menu(call)
        else:
            delete_message(message)
            question = f"Слово {TEST_CASES[uid][qn][0][0]} переводится на русский, как:"
            answers_markup = InlineKeyboardMarkup(row_width=2)
            buttons = list()
            for translation in TEST_CASES[uid][qn][1]:
                if translation == TEST_CASES[uid][qn][0][1]:
                    correct_answer = ('topic_test', tid - 1, qn + 1, True)
                    buttons.append(InlineKeyboardButton(translation, callback_data=dumps(correct_answer)))
                else:
                    incorrect_answer = ('topic_test', tid - 1, qn + 1, False)
                    buttons.append(InlineKeyboardButton(translation, callback_data=dumps(incorrect_answer)))
            answers_markup.add(buttons[0], buttons[1])
            answers_markup.add(buttons[2], buttons[3])
            answers_markup.add(InlineKeyboardButton(f'Меню темы', callback_data=dumps(('topic_menu', tid-1))))
            this_msg_id = bot.send_message(uid, question, reply_markup=answers_markup).id
            add_msg_to_del(uid, this_msg_id)
    except KeyError:
        topic_menu(call)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'topic_word')
def topic_word(call):
    """Выводит случайное слово из темы и его перевод."""
    data = loads(call.data)
    message = call.message
    uid = message.chat.id
    bot.answer_callback_query(call.id)
    delete_message(message)
    tid = data[1]
    rw = af.get_topic_word(my_engine, message.chat.id, tid)
    user_markup = InlineKeyboardMarkup()
    user_markup.add(InlineKeyboardButton(f'Меню темы', callback_data=dumps(('topic_menu', tid-1))))
    this_msg_id = bot.send_message(uid, text=f"На английском: {rw[0]}\nНа русском: {rw[1]}",
                                   reply_markup=user_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: loads(call.data)[0] == 'topic_words')
def topic_words(call):
    """Выводит список всех слов в теме."""
    bot.answer_callback_query(call.id)
    delete_message(call.message)
    uid = call.message.chat.id
    tid = loads(call.data)[1]
    tw = [('Слово', 'Перевод'), ] + af.get_words_in_topic(my_engine, tid)
    msg = tabulate(tw,  headers='firstrow')
    return_markup = InlineKeyboardMarkup()
    return_markup.add(InlineKeyboardButton('Меню темы', callback_data=dumps(('topic_menu', tid-1))))
    this_msg_id = bot.send_message(uid, msg, reply_markup=return_markup).id
    add_msg_to_del(uid, this_msg_id)


@bot.callback_query_handler(func=lambda call: True)
def last_handler(call):
    print('Перехвачено неопознанное сообщение.')


bot.polling(none_stop=True, timeout=0)
