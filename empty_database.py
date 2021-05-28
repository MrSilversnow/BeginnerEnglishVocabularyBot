def _drop_topics(engine):
    """Удаляет таблицу topics."""
    engine.execute("drop table if exists topics")


def _drop_words(engine):
    """Удаляет таблицу words."""
    engine.execute("drop table if exists words")


def _drop_users(engine):
    """Удаляет таблицу users."""
    engine.execute("drop table if exists users")


def drop_all_tables(engine):
    """Удаляет все таблицы."""
    _drop_users(engine)
    _drop_words(engine)
    _drop_topics(engine)
