from flask import Flask, render_template, request, make_response, redirect, session, url_for

from datetime import datetime, timedelta, timezone

app = Flask(__name__, template_folder='templates')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)
app.secret_key = 'EXA844'

@app.route('/')
def counter():
    if 'username' in session:
        username = session['username']
        running_time = (datetime.now(timezone.utc) - session.get('_creation_time'))
        remaining_time = app.permanent_session_lifetime - running_time
    if 'counter' in request.cookies:
        count = int(request.cookies.get('counter'))
    else:
        count = 1
    resp = make_response(render_template('counter.html', counter=count, username=username, remaining_time=remaining_time))
    resp.set_cookie('counter', str(count + 1).encode('utf-8'), max_age=60*60)
    return resp

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    session['_creation_time'] = datetime.now(timezone.utc)
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')