from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(_name_)
app.secret_key = 'your_secret_key'

# Create a database connection
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create a table to store questions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        correct_option INTEGER
    )
''')

# Add sample questions (you can add more)
cursor.executemany('''
    INSERT INTO questions (question_text, option1, option2, option3, option4, correct_option)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    ("What is the capital of France?", "Paris", "Berlin", "London", "Madrid", 1),
    ("What is 2 + 2?", "3", "4", "5", "6", 2),
])

conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = [int(request.form[f'q{i}']) for i in range(1, len(request.form) + 1)]
    
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT correct_option FROM questions")
    correct_answers = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    score = sum([1 for i, user_answer in enumerate(user_answers) if user_answer == correct_answers[i]])
    
    return render_template('result.html', score=score)

if _name_ == '_main_':
    app.run(debug=True)