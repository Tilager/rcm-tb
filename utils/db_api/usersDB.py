import logging
import sqlite3

from data.config import ADMINS


def addUser(uid, uname, acs):
    with sqlite3.connect('rcm-tg-bot.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id char(40) NOT NULL PRIMARY KEY,
                user_name char(70) NOT NULL,
                access INT not null,
                code char(10)
        )""")

        connect.commit()

        if not getUser(uid):
            connect.execute(f"""INSERT INTO users (user_id, user_name, access) 
            VALUES ('{uid}', '{uname}', {acs})""")
            connect.commit()
            logging.info(f'User {uname} ::: {uid} created in DB.')

        cursor.close()


def getUser(uid):
    with sqlite3.connect('rcm-tg-bot.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"select * from users where user_id = {uid}")
        data = cursor.fetchone()

        cursor.close()

    return data


def setCode(uid, code):
    with sqlite3.connect('rcm-tg-bot.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"UPDATE users set code = '{code}' where user_id='{uid}'")

        cursor.close()


def setAccess(uid, access):
    with sqlite3.connect('rcm-tg-bot.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"UPDATE users set access = '{access}' where user_id='{uid}'")

        cursor.close()


def shutdownAccess():
    with sqlite3.connect('rcm-tg-bot.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"UPDATE users set access = 0 where user_id not in ({', '.join(ADMINS)}) ")
        cursor.execute(f"UPDATE users set code = NULL where code is not NULL")
        logging.info('The database has been successfully edited!')

        cursor.close()
