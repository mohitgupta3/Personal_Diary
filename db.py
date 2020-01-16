import sqlite3
from cryptoUtils import CryptoUtils as cu
from datetime import datetime

class DB:
    def __init__(self):
        conn = sqlite3.connect("events_base.db", check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()

db = DB()

class UsersModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='users'")
        row = cursor.fetchone()
        if row is None:
            self.init_table()

    # def init_table(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute('''CREATE TABLE IF NOT EXISTS users
    #                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                          user_name VARCHAR(50),
    #                          password_hash VARCHAR(128),
    #                          admin INTEGER
    #                          )''')
    #     cursor.execute('''INSERT INTO users (user_name, password_hash, admin)
    #                       VALUES (?,?,?)''', ('admin', 'admin', 1))
        
    #     cursor.close()
    #     self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users
                          (user_name, password_hash, admin)
                          VALUES (?,?,?)''', (user_name, password_hash, 0))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_by_name(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class EventModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='event'")
        row = cursor.fetchone()
        if row is None:
            self.init_table()

    # def init_table(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute('''CREATE TABLE IF NOT EXISTS event
    #                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                          title VARCHAR(500),
    #                          content VARCHAR(2500),
    #                          user_id INTEGER,
    #                          pub_date INTEGER,
    #                          pic VARCHAR(100)
    #                          enckey VARCHAR(32)
    #                          )''')
    #     cursor.close()
    #     self.connection.commit()

    def insert(self, title, content, user_id, pic, edit=None):
        key = cu.gen_key()
        title = cu.encrypt(title, key)
        content = cu.encrypt(content, key)
        pub_date = round(datetime.timestamp(datetime.now()))
        if edit:
            event = EventModel(db.get_connection())
            if event.get(edit):
                pub_date = event.get(edit)[4]
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO event
                          (title, content, user_id, pub_date, pic, enckey)
                          VALUES (?,?,?,?,?)''', (title, content, str(user_id), pub_date, pic, key))
        order = ' ORDER BY pub_date DESC'
        cursor.execute("SELECT * FROM event WHERE user_id = ?" + order, (str(user_id),))
        cursor.close()
        self.connection.commit()

    def get(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM event WHERE id = ?", (str(event_id),))
        row = cursor.fetchone()
        title = row[0]
        content = row[1]
        uid = row[2]
        pubdate = row[3]
        pic = row[4]
        key = row[5]

        # Perform decryption...
        title = cu.decrypt(title, key)
        content = cu.decrypt(content, key)

        row = (title, content, uid, pubdate, pic, key)
        return row

    def get_all(self, user_id = None, sort=0):
        if sort == 0:
            order = ' ORDER BY pub_date DESC'
        elif sort == 1:
            order = ' ORDER BY title'
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM event WHERE user_id = ?" + order, (str(user_id),))
        else:
            cursor.execute("SELECT * FROM event" + order)
        rows = cursor.fetchall()
        for row in rows:
            title = row[0]
            content = row[1]
            uid = row[2]
            pubdate = row[3]
            pic = row[4]
            key = row[5]

            # Perform decryption...
            title = cu.decrypt(title, key)
            content = cu.decrypt(content, key)
        return rows

    def delete(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM event WHERE id = ?''', (str(event_id),))
        cursor.close()
        self.connection.commit()

