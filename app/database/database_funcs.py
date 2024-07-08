import sqlite3

from typing import NamedTuple


# -------------------
# создаем базы данных
# -------------------

# путь к БД
users_db = 'app/database/users.db'


# все пользователи и их настройки
def users_table_creation() -> None:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(
                       tg_id INT,
                       tg_username TEXT,
                       hits INT,
                       tries INT,
                       hit_rate DECIMAL(5, 2),
                       name TEXT,
                       is_public INT,
                       note TEXT
                       )""")
        db.commit()


# --------------------------------------
# дописываем и/или обновляем данные в БД
# --------------------------------------


# новый пользователь, добавляем его в общую базу
def new_user(tg_id: int, tg_username: str, users_name: str) -> None:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tg_id 
                       FROM users_data
                       WHERE tg_id = ?""",
                       [tg_id])
        already_exists = cursor.fetchone()
        if already_exists is None:
            cursor.execute("""INSERT INTO users_data
                           (tg_id, tg_username, hits, tries, hit_rate, name, is_public, note) 
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                           [tg_id, tg_username, 0, 0, 0, users_name, 1, ''])
        else:
            update_data(tg_id=tg_id, column_name='tg_username', new_value=tg_username)
        db.commit()


# изменение какого-либо значения
def update_data(tg_id: int, column_name: str, new_value: str or int) -> None:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute(f"""UPDATE users_data
                       SET {column_name} = ?
                       WHERE tg_id = ?""",
                       [new_value, tg_id])
        db.commit()


# ----------------------------
# достаем из баз нужные данные
# ----------------------------


# id всех пользователей
def get_all_users_ids() -> list[int]:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tg_id
                       FROM users_data""")
        ids = cursor.fetchall()
    return [tg_id[0] for tg_id in ids]


# данные пользователя
def get_data(tg_id: int, column_name: str) -> int | str:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT {column_name}
                       FROM users_data
                       WHERE tg_id = ?""",
                       [tg_id])
        stats = cursor.fetchone()[0]
    return stats


class UsersData(NamedTuple):
    tg_id: int
    hit_rate: float
    name: str


def global_top() -> list[UsersData]:
    with sqlite3.connect(users_db) as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT tg_id, hit_rate, name
                       FROM users_data
                       WHERE tries >= 50 and is_public = 1
                       ORDER BY hit_rate DESC""")
        data_from_database = cursor.fetchall()
    top_players_list = list()
    for user in data_from_database:
        users_tg_id, users_hit_rate, users_name = user
        top_players_list.append(UsersData(tg_id=users_tg_id,
                                          hit_rate=users_hit_rate,
                                          name=users_name))
    return top_players_list


# ----------------
# создание таблицы
# ----------------
users_table_creation()
