from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Function to create the database table if not exists
def create_table():
    conn = sqlite3.connect('code_snippets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS snippets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT,
                 language TEXT,
                 stdin TEXT,
                 source_code TEXT,
                 timestamp TEXT)''')
    conn.commit()
    conn.close()

# Function to insert a code snippet into the database
def insert_snippet(username, language, stdin, source_code, timestamp):
    conn = sqlite3.connect('code_snippets.db')
    c = conn.cursor()
    c.execute('''INSERT INTO snippets (username, language, stdin, source_code, timestamp)
                 VALUES (?, ?, ?, ?, ?)''', (username, language, stdin, source_code, timestamp))
    conn.commit()
    conn.close()

# Function to retrieve all code snippets from the database
def get_snippets():
    conn = sqlite3.connect('code_snippets.db')
    c = conn.cursor()
    c.execute('''SELECT username, language, stdin, source_code, timestamp FROM snippets''')
    snippets = c.fetchall()
    conn.close()
    return snippets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    language = request.form['language']
    stdin = request.form['stdin']
    source_code = request.form['source_code']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    insert_snippet(username, language, stdin, source_code, timestamp)
    
    return redirect(url_for('snippet_table'))

@app.route('/snippets')
def snippet_table():
    snippets = get_snippets()
    return render_template('snippets.html', snippets=snippets)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
