def add_topic(engine, name):
    """Добавляет новую тему в список тем."""
    name.strip()
    engine.execute(f"""insert into topics (name) values ('{name}')""")


def add_word(engine, eng_word, rus_word, topic):
    """Добавляет новое слово в словарь."""
    eng_word.strip()
    rus_word.strip()
    topic.strip()
    engine.execute(f"""insert into words (word_in_english, word_in_russian, topic) 
                    values ('{eng_word}', '{rus_word}', '{topic}')""")  # добавили слово в словарь
    engine.execute(f"alter table users add `{eng_word}` integer default 0")  # добавили слово в список изучаемого


def add_user(engine, uid, username):
    """Добавляет нового пользователя бота."""
    engine.execute(f"insert into users (uid, username) values ('{uid}', '{username}')")


def delete_topic(engine, name):
    """Удаляет тему из списка тем. При этом удаляются все слова из этой темы."""
    name.strip()
    engine.execute(f"delete from topics where name='{name}'")


def delete_word(engine, eng_word):
    """Удаляет слово из словаря."""
    eng_word.strip()
    engine.execute(f"delete from users where word_in_english='{eng_word}'")  # удалили слово из словаря
    engine.execute(f"alter table users drop column {eng_word}")  # удалили слово из списка изучаемого

