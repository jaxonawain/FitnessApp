from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def validate_session():
    if 'username' in session:
        return
    else:
        return render_template('login.html')


@app.route('/')
def render_index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/render_login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('render_index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('render_index'))


@app.route('/statistics')
def render_statistics_page():
    render_template('statistics.html')


app.run()
