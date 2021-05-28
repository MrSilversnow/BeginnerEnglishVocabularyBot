def _create_table_topics(engine):
    """Создает таблицу для тем."""
    engine.execute("""create table Topics(
                    id integer primary key auto_increment,
                    name varchar(120) unique
                    )""")


def _create_table_words(engine):
    """Создает таблицу для слов."""
    engine.execute("""create table Words(
                    word_in_english varchar(30) primary key,
                    word_in_russian varchar(30) unique,
                    topic integer,
                    foreign key (topic) references Topics (id) on delete cascade
                    )""")


def _create_table_users(engine):
    """Создает таблицу для пользователей и их прогресса."""
    engine.execute("""create table Users(
                    uid bigint unsigned primary key,
                    username varchar(30) unique 
                    # добавлять столбцы, отвечающие словам (на английском)
                    )""")


def create_all_tables(engine):
    """Создает все необходимые таблицы."""
    _create_table_topics(engine)
    _create_table_words(engine)
    _create_table_users(engine)
