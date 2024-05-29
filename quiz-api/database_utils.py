import sqlite3
import classes

databaseFile = 'db.db'

def insert_question(input_question):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        insertion = cur.execute(
            "INSERT INTO Questions (title, text, image, position) VALUES (?, ?, ?, ?)",
            (input_question.title, input_question.text, input_question.image, input_question.position)
        )
        conn.commit()
        
        for answer in input_question.possibleAnswers:
            insert_answer(answer, cur.lastrowid)
        
        return cur.lastrowid  # Assuming you want to return the ID of the inserted question
    
def insert_answer(input_answer, question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        insertion = cur.execute(
            "INSERT INTO Answers (text, isCorrect, questionId) VALUES (?, ?, ?)",
            (input_answer.text, input_answer.isCorrect, question_id)
        )
        conn.commit()
        
        return cur.lastrowid  # Assuming you want to return the ID of the inserted answer
    
def delete_question(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Questions WHERE id = ?", (question_id,))
        conn.commit()
        
def delete_answer(answer_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE id = ?", (answer_id,))
        conn.commit()
        
def delete_answers_for_question(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE questionId = ?", (question_id,))
        conn.commit()
    
def clear_questions():
    clear_answers()
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Questions")
        conn.commit()
        
def clear_answers():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers")
        conn.commit()
       
def get_answers(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Answers WHERE questionId = ?", (question_id,))
        answers = cur.fetchall()
        
        return [classes.Answer(text = answer[1], isCorrect = answer[2]) for answer in answers]
        
def get_questions():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions")
        questions = cur.fetchall()
        
        return [classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], possibleAnswers = get_answers(question[0])) for question in questions]
    
def get_question(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE id = ?", (question_id,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
def get_question_by_position(position):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE position = ?", (position,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
def update_question(question):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("UPDATE Questions SET title = ?, text = ?, image = ?, position = ? WHERE id = ?", (question.title, question.text, question.image, question.position, question.id))
        conn.commit()
        
        delete_answers_for_question(question.id)
        for answer in question.possibleAnswers:
            insert_answer(answer, question.id)
            
def does_question_exist(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Questions WHERE id = ?", (question_id,))
        return cur.fetchone()[0] > 0