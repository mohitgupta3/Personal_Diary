import os
import time
import getpass
import multiprocessing as mp

class setup:
    def install_dependencies(self):
        try:
            import flask
            import flask_wtf
            import sqlite3
            import pyaes
            import secrets
            import wtforms
            import PIL
        except:
            ImportError('\n\t[INFO] --> Need to install some packages!\n')
        finally:
            os.system('pip install flask')
            os.system('pip install flask-wtf')
            os.system('pip install wtforms')
            os.system('pip install pyaes')
            os.system('pip install pillow')
            os.system('pip install datetime')

            print('\n\n\t[INFO] --> All packages are now installed')

    def prepare_db(self):
        import sqlite3

        if (os.path.exists('events_base.db')):
            os.remove('events_base.db')
        else:
            pass
        
        conn = sqlite3.connect('events_base.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name VARCHAR(50),
                            password_hash VARCHAR(128),
                            admin INTEGER
                            )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS event
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title VARCHAR(500),
                            content VARCHAR(2500),
                            user_id INTEGER,
                            pub_date INTEGER,
                            pic VARCHAR(100),
                            enckey VARCHAR(32)
                            )''')

        admin_pass = getpass.getpass(prompt = '\tPlease create an admin password: ')
        admin_pass1 = getpass.getpass(prompt = '\tRe-enter the admin password: ')
        
        if(admin_pass == admin_pass1):
            conn.execute('''INSERT OR IGNORE INTO users (user_name, password_hash, admin)
                            VALUES (?,?,?)''', ('admin', admin_pass, 1))
            print('\n\tAdmin Username: administrator\n\tPassword: '+admin_pass)
            time.sleep(3)
        
        else:
            print('\n\tERROR!: Passwords mismatch. Please try again.\n')
            self.prepare_db(self)

    def run_app(self):
        os.system('python Run.py')

    def show_docs(self):
        os.system('docs.html')

    def main(self):
        self.install_dependencies()
        self.prepare_db()

if __name__ == "__main__":
    stp = setup()
    stp.main()
    
    open_docs = mp.Process(name = 'PersonalDiaryDocs', target = stp.show_docs)
    run_app = mp.Process(name = 'run', target = stp.run_app)
    
    open_docs.start()
    run_app.start() 

    exit()
