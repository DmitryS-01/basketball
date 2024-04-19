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
                       user_id INT,
                       tries INT,
                       hits INT
                       )""")
        db.commit()


# --------------------------------------
# дописываем и/или обновляем данные в БД
# --------------------------------------


# новый пользователь, добавляем его в общую базу
def new_user(user_id):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT user_id 
                       FROM users 
                       WHERE user_id = ?""",
                       [user_id])
        already_exists = cursor.fetchone()
        if already_exists is None:
            cursor.execute("""INSERT INTO users
                           (user_id, tries, hits) 
                           VALUES(?, ?, ?)""",
                           [user_id, 0, 0])
        db.commit()


# переписываю --историю-- стату
def new_shot(user_id, hit):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tries, hits
                               FROM users
                               WHERE user_id = ?""",
                       [user_id])
        tries, hits = cursor.fetchall()[0]
        cursor.execute("""UPDATE users
                       SET (tries, hits) = (?, ?)
                       WHERE user_id = ?""",
                       [tries + 1, hits + 1 if hit else hits, user_id])
        db.commit()


# ----------------------------
# достаем из баз нужные данные
# ----------------------------


# данные пользователя
def data(user_id):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tries, hits
                       FROM users
                       WHERE user_id = ?""",
                       [user_id])
        stats = cursor.fetchall()
    return stats[0]


if __name__ == '__main__':
    users_table_creation()
