from create_database import create_all_tables
from empty_database import drop_all_tables
from update_tables import add_topic, add_word, add_user


def _refill_database(engine):
    """Пересоздает пустыми все таблицы в базе данных."""
    drop_all_tables(engine)
    create_all_tables(engine)


def _fill_topics(engine):
    """Заполняет список тем."""
    add_topic(engine, 'Погода')
    add_topic(engine, 'Семья')
    add_topic(engine, 'Внешность')
    add_topic(engine, 'Характер')


def _fill_weather_words(engine):
    tid = '1'
    add_word(engine, 'weather', 'погода', tid)
    add_word(engine, 'fine', 'прекрасный', tid)
    add_word(engine, 'terrible', 'ужасный', tid)
    add_word(engine, 'cold', 'холодный', tid)
    add_word(engine, 'hot', 'жаркий', tid)
    add_word(engine, 'warm', 'теплый', tid)
    add_word(engine, 'the sky', 'небо', tid)
    add_word(engine, 'the sun', 'солнце', tid)
    add_word(engine, 'rain', 'дождь', tid)
    add_word(engine, 'wind', 'ветер', tid)
    add_word(engine, 'cloud', 'облако', tid)
    add_word(engine, 'snow', 'снег', tid)
    add_word(engine, 'sunny', 'солнечный', tid)
    add_word(engine, 'rainy', 'дождливый', tid)
    add_word(engine, 'windy', 'ветреный', tid)
    add_word(engine, 'cloudy', 'облачный', tid)
    add_word(engine, 'bright', 'яркий', tid)
    add_word(engine, 'snowy', 'снежный', tid)
    add_word(engine, 'to rain', 'дождить', tid)
    add_word(engine, 'to snow', 'снежить', tid)
    add_word(engine, 'to blow', 'дуть', tid)
    add_word(engine, 'to shine', 'светить', tid)
    add_word(engine, 'to get warmer', 'теплеть', tid)
    add_word(engine, 'to get colder', 'холодать', tid)


def _fill_family_words(engine):
    tid = '2'
    add_word(engine, 'father', 'отец', tid)
    add_word(engine, 'mother', 'мать', tid)
    add_word(engine, 'parents', 'родители', tid)
    add_word(engine, 'son', 'сын', tid)
    add_word(engine, 'daughter', 'дочь', tid)
    add_word(engine, 'sister', 'сестра', tid)
    add_word(engine, 'brother', 'брат', tid)
    add_word(engine, 'cousin', 'двоюродный брат/сестра', tid)
    add_word(engine, 'sibling', 'родной брат/сестра', tid)
    add_word(engine, 'second cousin', 'троюродный брат/сестра', tid)
    add_word(engine, 'twins', 'близнецы', tid)
    add_word(engine, 'aunt', 'тетя', tid)
    add_word(engine, 'uncle', 'дядя', tid)
    add_word(engine, 'nephew', 'племянник', tid)
    add_word(engine, 'niece', 'племянница', tid)
    add_word(engine, 'grandfather', 'дедушка', tid)
    add_word(engine, 'grandmother', 'бабушка', tid)
    add_word(engine, 'grandparents', 'дедушка и бабушка', tid)
    add_word(engine, 'great grandmother', 'прабабушка', tid)
    add_word(engine, 'great grandfather', 'прадедушка', tid)
    add_word(engine, 'grandson', 'внук', tid)
    add_word(engine, 'granddaughter', 'внучка', tid)
    add_word(engine, 'husband', 'муж', tid)
    add_word(engine, 'wife', 'жена', tid)
    add_word(engine, 'child', 'ребенок', tid)
    add_word(engine, 'children', 'дети', tid)
    add_word(engine, 'grandchildren', 'внуки', tid)
    add_word(engine, 'baby', 'малыш', tid)
    add_word(engine, 'relative', 'родственник', tid)


def _fill_appearance(engine):
    tid = '3'
    add_word(engine, 'nice', 'милый', tid)
    add_word(engine, 'pretty', 'хорошенькая', tid)
    add_word(engine, 'beautiful', 'красивая', tid)
    add_word(engine, 'handsome', 'красивый', tid)
    add_word(engine, 'good-looking', 'приятной внешности', tid)
    add_word(engine, 'plain', 'простой внешности', tid)
    add_word(engine, 'ugly', 'уродливый', tid)
    add_word(engine, 'appearance', 'внешность', tid)
    add_word(engine, 'height', 'рост', tid)
    add_word(engine, 'tall', 'высокий', tid)
    add_word(engine, 'short', 'низкий', tid)
    add_word(engine, 'middle-sized', 'среднего роста', tid)
    add_word(engine, 'build', 'телосложение', tid)
    add_word(engine, 'thin', 'худой', tid)
    add_word(engine, 'fat', 'толстый', tid)
    add_word(engine, 'slim', 'стройная', tid)
    add_word(engine, 'athletic', 'мускулистый', tid)
    add_word(engine, 'hair colour', 'цвет волос', tid)
    add_word(engine, 'fair hair', 'светлые волосы', tid)
    add_word(engine, 'dark hair', 'темные волосы', tid)
    add_word(engine, 'black hair', 'черные волосы', tid)
    add_word(engine, 'brown hair', 'коричневые волосы', tid)
    add_word(engine, 'red hair', 'рыжие волосы', tid)
    add_word(engine, 'blond hair', 'очень светлые волосы', tid)
    add_word(engine, 'hair', 'волосы', tid)
    add_word(engine, 'short hair', 'короткие волосы', tid)
    add_word(engine, 'long hair', 'длинные волосы', tid)
    add_word(engine, 'straight hair', 'прямые волосы', tid)
    add_word(engine, 'wavy hair', 'волнистые волосы', tid)
    add_word(engine, 'curly hair', 'кудрявые волосы', tid)
    add_word(engine, 'thick hair', 'густые волосы', tid)
    add_word(engine, 'thin hair', 'редкие волосы', tid)
    add_word(engine, 'eyes', 'глаза', tid)
    add_word(engine, 'face', 'лицо', tid)
    add_word(engine, 'nose', 'нос', tid)
    add_word(engine, 'mouth', 'рот', tid)
    add_word(engine, 'lips', 'губы', tid)
    add_word(engine, 'teeth', 'зубы', tid)
    add_word(engine, 'ears', 'уши', tid)
    add_word(engine, 'forehead', 'лоб', tid)
    add_word(engine, 'neck', 'шея', tid)
    add_word(engine, 'body', 'тело', tid)
    add_word(engine, 'arms', 'руки', tid)
    add_word(engine, 'hands', 'кисти', tid)
    add_word(engine, 'legs', 'ноги', tid)
    add_word(engine, 'knees', 'колени', tid)
    add_word(engine, 'feet', 'ступни', tid)


def _fill_character(engine):
    tid = '4'
    add_word(engine, 'typical', 'типичный', tid)
    add_word(engine, 'close', 'близкий', tid)
    add_word(engine, 'loving', 'любящий', tid)
    add_word(engine, 'friendly', 'дружелюбный', tid)
    add_word(engine, 'caring', 'заботливый', tid)
    add_word(engine, 'independent', 'независимый', tid)
    add_word(engine, 'smart', 'сообразительный', tid)
    add_word(engine, 'clever', 'умный', tid)
    add_word(engine, 'serious', 'серьезный', tid)
    add_word(engine, 'kind', 'добрый', tid)
    add_word(engine, 'lazy', 'ленивый', tid)
    add_word(engine, 'busy', 'деловой', tid)
    add_word(engine, 'bossy', 'любящий командовать', tid)
    add_word(engine, 'naughty', 'непослушный', tid)
    add_word(engine, 'noisy', 'шумный', tid)
    add_word(engine, 'creative', 'творческий', tid)
    add_word(engine, 'strong character', 'сильный характер', tid)
    add_word(engine, 'brave', 'храбрый', tid)
    add_word(engine, 'active', 'активный', tid)
    add_word(engine, 'quiet', 'тихий', tid)
    add_word(engine, 'angry', 'злой/сердитый', tid)
    add_word(engine, 'talkative', 'разговорчивый', tid)
    add_word(engine, 'helpful', 'полезный', tid)
    add_word(engine, 'tidy', 'аккуратный', tid)
    add_word(engine, 'polite', 'вежливый', tid)
    add_word(engine, 'silly', 'глупый', tid)
    add_word(engine, 'honest', 'честный', tid)
    add_word(engine, 'curious', 'любопытный', tid)
    add_word(engine, 'shy', 'застенчивый', tid)
    add_word(engine, 'sociable', 'общительный', tid)


def _fill_words(engine):
    """Заполняет список слов."""
    _fill_weather_words(engine)
    _fill_family_words(engine)
    _fill_appearance(engine)
    _fill_character(engine)


def _fill_users(engine):
    """Заполняет список пользователей"""
    add_user(engine, '402578968', 'mr_silversnow')
    add_user(engine, '492546877', 'AlexandrTretyakov')


def create_test_sample(engine):
    """Создает тестовый экземпляр базы данных."""
    _refill_database(engine)
    _fill_topics(engine)
    _fill_words(engine)
    _fill_users(engine)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    my_engine = create_engine('mysql+pymysql://root:password@localhost:3306/bot')
    create_test_sample(my_engine)
