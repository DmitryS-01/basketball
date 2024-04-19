import sqlite3
import os


# -------------------
# создаем базы данных
# -------------------


# все файлы БД

# папка
databases_dir = os.path.dirname(__file__)

# файлы БД
stats_db = os.path.join(databases_dir, 'stats.db')


# все пользователи и их настройки
def users_table_creation():
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       user_id TEXT,
                       hits INT,
                       tries INT
                       )""")
        db.commit()


# --------------------------------------
# дописываем и/или обновляем данные в БД
# --------------------------------------


# новый пользователь, добавляем его в общую базу
def new_user(user_id):
    username_tg = f'@{user_id}' if user_id is not None else None
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT user_id 
                       FROM users 
                       WHERE user_id = ?""",
                       [user_id])
        already_exists = cursor.fetchone()
        if already_exists is None:
            cursor.execute("""INSERT INTO users
                           (chat_id, user_id, hits, tries) 
                           VALUES(?, ?, ?)""",
                           [user_id, 0, 0])
        db.commit()


# переписываю --историю-- стату
def new_shot(user_id, hit):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT tries, hits
                       FROM users
                       WHERE user_id = ?"""
                       [user_id])
        tries, hits = cursor.fetchall()
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE users
                       SET (hits, tries) = (?, ?)
                       WHERE user_id = ?""",
                       [hits + 1 if hit else hits, tries + 1, user_id])
        db.commit()



# ----------------------------
# достаем из баз нужные данные
# ----------------------------


# данные пользователя
def data(user_id):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT hits, tries
                       FROM users
                       WHERE user_id = ?""",
                       [user_id])
        users = cursor.fetchall()
    users_tuple = tuple(user[0] for user in users)
    return users_tuple


if __name__ == '__main__':
    pass
