#Campo escondido
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')
@app.route('/')
def counter():
counter_value = request.args.get('counter',default=0, type=int) + 1
return render_template('counter.html', counter=counter_value)
if __name__ == '__main__':
app.run(debug=True)

#Cookie
from flask import Flask, render_template, request, make_response
app = Flask(__name__, template_folder='templates')
@app.route('/')
def counter():
if 'counter' in request.cookies:
count = int(request.cookies.get('counter'))
else:
count = 1
resp = make_response(render_template('counter.html', counter=count))
resp.set_cookie('counter', str(count + 1).encode('utf-8'), max_age=60*60)
return resp
if __name__ == '__main__':
app.run(debug=True)

#sessoes

from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta, timezone
app = Flask(__name__, template_folder='templates')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)
app.secret_key = 'EXA844'
@app.route('/')
def home():
if 'username' in session:
username = session['username’]
running_time = (datetime.now(timezone.utc) - session.get('_creation_time'))
remaining_time = app.permanent_session_lifetime - running_time
return f'Hello, {username}! Your session will expire in '+
str(remaining_time)+' seconds. <a href="/logout">Logout</a>'
else:
return 'Welcome to Flask Session Example! <a href="/login">Login</a>’

@app.route('/login', methods=['POST'])
def login():
username = request.form['username']
session['username'] = username
session['_creation_time'] = datetime.now(timezone.utc)
return redirect('/')
if __name__ == '__main__':
app.run(debug=True)