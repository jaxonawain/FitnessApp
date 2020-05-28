from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def render_index():
    return render_template('index.html', username='Jakson')

@app.route('/edit')
def render_edit_page():
    return render_template('edit.html')

@app.route('/statistics')
def render_statistics_page():
    return render_template('statistics.html')


app.run()
