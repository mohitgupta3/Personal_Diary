import multiprocessing
import time
import webbrowser
import application
import sqlite3
import os

def prepare_db(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_name VARCHAR(50),
                                password_hash VARCHAR(128),
                                admin INTEGER
                                )''')

    connection.execute('''CREATE TABLE IF NOT EXISTS event
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title VARCHAR(500),
                                content VARCHAR(2500),
                                user_id INTEGER,
                                pub_date INTEGER,
                                pic VARCHAR(100),
                                enckey VARCHAR(32)
                                )''')

def create_admin(conn):
    admin_pass = input('Please create an admin password: ')
    admin_pass1 = input('Re-enter the admin password: ')
    if(admin_pass == admin_pass1):
        conn.execute('''INSERT INTO users (user_name, password_hash, admin)
                          VALUES (?,?,?)''', ('administrator', admin_pass, 1))
        print('\n\tAdmin Username: administrator\nPassword: '+admin_pass)
    else:
        print('\n\tERROR!: Passwords mismatch. Please try again.\n')
        create_admin()

def check_for_db():
    print('Checking for database...')
    conn = sqlite3.connect('events_base.db')
    prepare_db(conn)
    create_admin(conn)

def run_application():
    application.run()

def open_browser():
    url = 'http://127.0.0.1:8080/'
    webbrowser.open(url)

if __name__ == '__main__':
    print('\n\tStart... ')
    check_for_db()

    p0 = multiprocessing.Process(name = 'app', target = run_application)
    p1 = multiprocessing.Process(name = 'web', target = open_browser)
    
    p0.start()
    p1.start()
