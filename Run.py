import multiprocessing
import time
import webbrowser
import application
import os

def dlt_setup():
    if(os.path.exists('setup.py')):
        os.remove('setup.py')
    else:
        pass
    
    if(os.path.exists('setup.cmd')):
        os.remove('setup.cmd')
    else:
        pass
    
def run_application():
    application.run()

def open_browser():
    time.sleep(6)
    url = 'http://127.0.0.1:8080/'
    webbrowser.open(url)

if __name__ == '__main__':
    print('\n\tStart... ')
    
    dlt_setup()

    os.system('mode con: cols=95 lines=35')

    p0 = multiprocessing.Process(name = 'app', target = run_application)
    p1 = multiprocessing.Process(name = 'web', target = open_browser)
    
    p0.start()
    p1.start()
