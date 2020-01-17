# Personal_Diary

#### Note: _This project is in runnable condition but some features are still experimental or still under active development. Please report bugs in the issues column._

This is a simple personal diary application written in Python3 with flask.
It provides/will provide the following features:
1. Multiple accounts support with password protection.
2. All entries are protected with AES 256-bit encryption. _(under testing)_
3. Statistics for all users. (Admin access only)
4. Support for adding images with diary entries.
5. AI driven auto text completion. _(future)_
6. Lets you set administrator password during installation.

### First Run:

You need _python 3.6+_ to run this application.

Perform the steps given below if you are running the application for the first time.
1. Hit _Setup.cmd_ or type in the console
  For Windows:
```
python setup.py
```
  For Ubuntu:
 ```
 python3 setup.py
 ```
 This will install all the dependencies and set up the admin account.
 
### To start the project:
1. Install required packages (if necessary) by simply executing the following command in your terminal.
   
  For Windows:
```
    pip install <package-name>
```
  For Ubuntu:
```
    pip3 install <package-name>
```

2. Hit *Run.cmd (windows) or Run.sh (ubuntu)* to start the application.
    or simply type *python Run.py (windows)* or *python3 Run.py (ubuntu)* in terminal and hit enter.
    
 It will run the application and open the diary application in your default browser after 3 seconds.
