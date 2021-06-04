def select_column_names(engine, table_name):
    """Позволяет получить упорядоченный список названий столбцов таблицы table_name."""
    result = engine.execute(f"""select distinct column_name from INFORMATION_SCHEMA.COLUMNS where 
                            table_name='{table_name}' and table_schema='bot' order by ordinal_position""").fetchall()
    result = [tuple(res[0] for res in result), ]
    return result


def select_topic(engine, tid=None, name=None):
    """Позволяет получить таблицу (или её часть) topics."""
    if tid is None and name is None:
        result = engine.execute("select * from topics order by id")
    elif name is None:
        result = engine.execute(f"select * from topics where id='{tid}'")
    elif tid is None:
        result = engine.execute(f"select * from topics where name='{name}'")
    else:
        result = engine.execute(f"select * from topics where id='{tid}' and name='{name}'")
    return result.fetchall()


def select_word(engine, word=None):
    """Позволяет получить таблицу (или её часть) words."""
    if word is None:
        result = engine.execute("select * from words")
    else:
        result = engine.execute(f"select * from words where word_in_english='{word}'")
    return result.fetchall()


def select_user(engine, uid=None, username=None):
    """Позволяет получить таблицу (или её часть) users."""
    if uid is None and username is None:
        result = engine.execute("select * from users")
    elif username is None:
        result = engine.execute(f"select * from users where uid='{uid}'")
    elif uid is None:
        result = engine.execute(f"select * from users where username='{username}'")
    else:
        result = engine.execute(f"select * from users where uid='{uid}' and username='{username}'")
    return result.fetchall()


def select_users_score(engine, uid, eng_word):
    """Позволяет получить статистику пользователя uid по конкретному слову eng_word."""
    result = engine.execute(f"select `{eng_word}` from users where uid='{uid}'")
    return result.fetchall()




