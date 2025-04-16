from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'ucat_scores.db'

# Initialize the SQLite database and table if not already created.
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if request.method == 'POST':
        score = request.form.get('score')
        if score:
            try:
                score = int(score)
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('INSERT INTO scores (date, score) VALUES (?, ?)', (date, score))
                conn.commit()
            except ValueError:
                # In a complete app, you might add error messages here.
                pass
        return redirect(url_for('index'))
    c.execute('SELECT * FROM scores ORDER BY id DESC')
    scores = c.fetchall()
    conn.close()
    return render_template('index.html', scores=scores)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)