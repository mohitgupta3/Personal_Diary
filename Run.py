import multiprocessing
import time
import webbrowser
import application

def run_application():
    application.run()

def open_browser():
     url = 'http://127.0.0.1:8080/'
     webbrowser.open(url)

if __name__ == '__main__':
    p0 = multiprocessing.Process(name = 'app', target = run_application)
    p1 = multiprocessing.Process(name = 'web', target = open_browser)
    
    p0.start()
    p1.start()