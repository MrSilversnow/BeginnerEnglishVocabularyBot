from select_tables import *
from update_tables import update_score, add_user
import random


def get_random_word(engine, uid):
    """Возвращает случайное слово с переводом в виде кортежа."""
    # Получаем все слова и частоту их правильного угадывания.
    column_names = select_column_names(engine, 'users')[0][2:]
    words_frequency = list(select_user(engine, uid=uid)[0][2:])
    # Создаем рулетку для распределения шансов для каждого слова.
    for i in range(len(words_frequency)):
        words_frequency[i] = 1 / (words_frequency[i]+1)
    frequency_roulette = sum(words_frequency)
    chosen_number = random.uniform(0, frequency_roulette)
    # Используем рулетку для распределения шансов для каждого слова.
    start = 0
    end = words_frequency[0]
    wie = None
    for i in range(len(words_frequency)-1):
        if start <= chosen_number <= end:
            wie = i
            break
        else:
            start += words_frequency[i]
            end += words_frequency[i+1]
    if wie is None:
        wie = random.randint(0, len(words_frequency)-1)
    random_word = select_word(engine, column_names[wie])[0]
    random_word = random_word[:-1]
    return random_word


def get_topic_word(engine, uid, tid):
    """Возвращает случайное слово по теме с id=tid."""
    # Выделяем нужные нам слова и частоту их правильного угадывания.
    words = select_word(engine)
    topic_words = [word[0] for word in words if word[-1] == tid]
    topic_words_frequency = list()
    column_names = select_column_names(engine, 'users')[0][2:]
    words_frequency = select_user(engine, uid=uid)[0][2:]
    for i in range(len(column_names)):
        if column_names[i] in topic_words:
            topic_words_frequency.append(words_frequency[i])
    # Создаем рулетку для распределения шансов для каждого слова.
    for i in range(len(topic_words_frequency)):
        topic_words_frequency[i] = 1 / (topic_words_frequency[i]+1)
    frequency_roulette = sum(topic_words_frequency)
    chosen_number = random.uniform(0, frequency_roulette)
    # Используем рулетку для распределения шансов для каждого слова.
    start = 0
    end = topic_words_frequency[0]
    wie = None
    for i in range(len(topic_words_frequency)-1):
        if start <= chosen_number <= end:
            wie = i
            break
        else:
            start += topic_words_frequency[i]
            end += topic_words_frequency[i+1]
    random_topic_word = select_word(engine, topic_words[wie])[0]
    random_topic_word = random_topic_word[:-1]
    return random_topic_word


def get_words_in_topic(engine, tid):
    """Возвращает список слов в теме с id=tid."""
    words = select_word(engine)
    topic_words = [word[:-1] for word in words if word[-1] == tid]
    return topic_words


def get_topic_test(engine, tid):
    """
    Возвращает слова, сгруппированные для теста по теме с id=tid в виде списка кортежей из двух кортежей:
    (eng_word, correct_translation), (random_translation, random_translation, random_translation, random_translation).
    """
    words_in_topic = get_words_in_topic(engine, tid)
    random.shuffle(words_in_topic)
    nowit = len(words_in_topic)
    topic_test = list()
    for i in range(nowit):
        first_tuple = words_in_topic[i]
        second_tuple = [i, ]
        noa = 0
        while noa != 3:
            rand_number = random.randint(0, nowit-1)
            if rand_number not in second_tuple:
                second_tuple.append(rand_number)
                noa += 1
        random.shuffle(second_tuple)
        second_tuple = tuple(words_in_topic[j][1] for j in second_tuple)
        topic_test.append(tuple((first_tuple, second_tuple)))
    return topic_test


def get_random_test(engine, uid, now=10):
    """
    Возвращает слова, сгруппированные для теста из now слов в виде списка кортежей из двух кортежей:
    (eng_word, correct_translation), (random_translation, random_translation, random_translation, random_translation).
    Использует аналитически-случайный подбор наименее изученых слов.
    """
    # Выбрали нужное количество слов для теста
    words = list()
    while len(words) != now:
        new_word = get_random_word(engine, uid)
        if new_word not in words:
            words.append(new_word)
    # Наберем всякого мусора для неправильных ответов
    random_test = list()
    incorrect_words = select_word(engine)
    incorrect_words = [word[1] for word in incorrect_words if word[0] not in words]
    for i in range(now):
        at = list()
        while len(at) != 3:
            answer = random.choice(incorrect_words)
            if answer not in at:
                at.append(answer)
        at.append(words[i][1])
        random.shuffle(at)
        random_test.append((words[i], tuple(at)))
    return random_test


def correct_answer(engine, uid, word_in_eng):
    """Увеличивает на 1 количество угадываний слова word_in_eng пользователем uid, но не выше 10."""
    if select_users_score(engine, uid, word_in_eng)[0][0] != 10:
        update_score(engine, uid, word_in_eng, 1)


def incorrect_answer(engine, uid, word_in_eng):
    """Уменьшает на 1 количество угадываний слова word_in_eng пользователем uid, но не ниже 0."""
    if select_users_score(engine, uid, word_in_eng)[0][0] != 0:
        update_score(engine, uid, word_in_eng, -1)


def get_topic_statistic(engine, uid, tid):
    """Позволет получить количество слов, изученных пользователем с uid."""
    words = select_column_names(engine, 'users')[0][2:]
    statistic = select_user(engine, uid)[0][2:]
    wit = get_words_in_topic(engine, tid)
    wit = tuple(word[0] for word in wit)
    n = len(wit)
    m = 0
    for wn in range(len(words)):
        if words[wn] in wit:
            if statistic[wn] == 10:
                m += 1
    return tuple((m, n))


def add_user_if_not_exist(engine, uid, username):
    """Добавляет пользователя, если его не существует."""
    if len(select_user(engine, uid)) == 0:
        add_user(engine, uid, username)
