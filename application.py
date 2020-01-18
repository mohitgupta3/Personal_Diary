from datetime import datetime
from addeventform import EventForm
from db import DB, UsersModel, EventModel
from flask import Flask, session, redirect, flash, render_template, url_for, request
from loginform import LoginForm
from registerform import RegisterForm
from PIL import Image
import win32com.client
import webbrowser
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
edit = None
read = None
db = DB()

def speak(text, rate = 1):    
    speak = win32com.client.Dispatch('Sapi.SpVoice')
    speak.Volume = 100
    speak.Rate = rate
    speak.Speak(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_error = ''
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        user = users.exists(form.username.data, form.password.data)
        if user[0]:
            session['userid'] = users.get(user[1])[0]
            session['username'] = users.get(user[1])[1]
            session['admin'] = users.get(user[1])[3]
            session['sort'] = 0
            speak('Login approved!')
            return redirect('/')
        else:
            login_error = 'Invalid Login Cradentials.'
            speak('Invalid Login Cradentials.')
    return render_template('login.html', title='My Diary', brand="Personal Diary", form=form, login_error=login_error)


@app.route('/')
def index():
    if "username" not in session:
        return redirect('/login')
    event = EventModel(db.get_connection())
    all_events = []
    for i in event.get_all(session['userid'], session['sort']):
        all_events.append({'pic': Image.open("static/img/" + i[5]) if i[5] != "0" else i[5], 'pub_date': datetime.fromtimestamp(i[4]).strftime('%d.%m.%Y %H:%M'),
                        'content': i[2], 'title': i[1], 'nid': i[0]})
    return render_template('index.html', title='Personal Diary', events=all_events, Image=Image, os=os)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if "username" not in session:
        return redirect('/login')
    event = EventModel(db.get_connection())

    global edit
    if not edit:
        form = EventForm()
    else:
        form = EventForm(event.get(edit))

    if form.validate_on_submit():
        event.insert(form.title.data if form.title.data != '' else event.get(edit)[1] if edit else "",
                    form.content.data if form.content.data != '' else event.get(edit)[2] if edit else "",
                    session['userid'],
                    form.picture.data.filename if form.picture.has_file() else "0" if not edit else event.get(edit)[5],
                    edit)

        print(form.picture.data.filename) if form.picture.has_file() else print("0")

        if form.picture.has_file():
            with open('static/img/' + form.picture.data.filename, "wb") as image:
                image.write(form.picture.data.read())

        if edit:
            delete(edit)
            edit = None

        return redirect('/')
    return render_template('addEvent.html', title = 'Personal Diary', form=form)


@app.route('/delete_event/<nid>')
def delete(nid):
    if "username" not in session:
        return redirect('/login')
    event = EventModel(db.get_connection())
    event.delete(nid)
    speak('event deleted!')
    return redirect('/')


@app.route('/edit_event/<nid>')
def editEvent(nid):
    if "username" not in session:
        return redirect('/login')
    event = EventModel(db.get_connection())
    global edit
    edit = nid
    return redirect("/add_event")

def readEvent(event):
    event = EventModel(db.get_connection())
    speak(event)

@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        users.insert(form.username.data, form.password.data)
        speak('registration successful!')
        flash('You have successfully registered', 'success')
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/admin')
def admin():
    if "username" not in session or session['admin'] != 1:
        flash('Access is denied', 'danger')
        return redirect('/')
    event, users = EventModel(db.get_connection()), UsersModel(db.get_connection())
    names, amount = {}, {}
    for n in event.get_all():
        if n[3] in amount:
            amount[n[3]] += 1
        else:
            names[n[3]] = users.get(n[3])[1]
            amount[n[3]] = 1
    return render_template('admin.html', title='User statistics',
                           amount=amount, names=names)


@app.route('/sort/<sort>')
def sortedevent(sort):
    if not "username" in session:
        return redirect('/login')
    speak('Sorting events!')
    session['sort'] = int(sort)
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('admin', None)
    speak('you have successfully logged out from the application')
    return redirect('/')

def run():
    os.system('title Personal diary application...')
    os.system('cls')
    speak('Please keep this window open to ensure smooth functioning of this application.')
    print('\n\tPlease keep this window open to ensure smooth functioning of this application...\n\n\tPress the (x) button on top of this window to exit the application.\n\n')
    app.run(port = 8080, host = '127.0.0.1')

if __name__ == '__main__':
    run()
