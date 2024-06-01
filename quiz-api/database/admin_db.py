import sqlite3
from config import Config
from utils.classes import Question, Answer

# Rebuilds the database, dropping all tables and recreating them
def rebuild_db():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Answers")
        cur.execute("DROP TABLE IF EXISTS Questions")
        cur.execute("DROP TABLE IF EXISTS Participations")
        conn.commit()
        
        cur.execute("CREATE TABLE Questions (id INTEGER PRIMARY KEY, position INTEGER, title TEXT, text TEXT, image TEXT)")
        cur.execute("CREATE TABLE Answers (id INTEGER PRIMARY KEY, text TEXT, isCorrect INTEGER, questionId INTEGER, FOREIGN KEY(questionId) REFERENCES Questions(id) ON DELETE CASCADE)")
        cur.execute("CREATE TABLE Participations (id INTEGER PRIMARY KEY, playerName TEXT, score INTEGER)")
        conn.commit()
        
# Inserts a question into the database
def insert_question(input_question):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        # Find the maximum position
        cur.execute("SELECT MAX(position) FROM Questions")
        max_position = cur.fetchone()[0]
        max_position = max_position if max_position is not None else 0

        # Ensure the position is not too far (e.g., if questions go from 1 to 5 and you try to add at 8, it will be set to 6)
        if input_question.position > max_position + 1:
            input_question.position = max_position + 1

        # Step 1: Ensure continuous numbering
        if input_question.position <= max_position:
            cur.execute(
                "UPDATE Questions SET position = position + 1 WHERE position >= ? AND position <= ?",
                (input_question.position, max_position)
            )
        
        # Step 2: Insert the new question at the desired position
        cur.execute(
            "INSERT INTO Questions (title, text, image, position) VALUES (?, ?, ?, ?)",
            (input_question.title, input_question.text, input_question.image, input_question.position)
        )
        conn.commit()
        
        new_question_id = cur.lastrowid
        
        # Insert possible answers
        for answer in input_question.possibleAnswers:
            insert_answer(answer, new_question_id)
        
        return new_question_id
    
    # Inserts an answer into the database
def insert_answer(input_answer, question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        insertion = cur.execute(
            "INSERT INTO Answers (text, isCorrect, questionId) VALUES (?, ?, ?)",
            (input_answer.text, input_answer.isCorrect, question_id)
        )
        conn.commit()
        
        return cur.lastrowid
    
# Deletes a question from the database
def delete_question(question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        # Get the position of the question to be deleted
        cur.execute("SELECT position FROM Questions WHERE id = ?", (question_id,))
        position = cur.fetchone()[0]

        # Delete the question
        cur.execute("DELETE FROM Questions WHERE id = ?", (question_id,))
        conn.commit()

        # Shift positions of the remaining questions
        cur.execute(
            "UPDATE Questions SET position = position - 1 WHERE position > ?",
            (position,)
        )
        conn.commit()
        
# Deletes an answer from the database   
def delete_answer(answer_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE id = ?", (answer_id,))
        conn.commit()
       
# Deletes all answers for a question 
def delete_answers_for_question(question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE questionId = ?", (question_id,))
        conn.commit()
   
# Deletes all questions from the database 
def clear_questions():
    clear_answers()
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Questions")
        conn.commit()
       
# Deletes all answers from the database 
def clear_answers():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers")
        conn.commit()
        
# Deletes all participations from the database
def clear_participations():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Participations")
        conn.commit()
        
# Updates a question in the database
def update_question(question):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        # Get the current position of the question
        cur.execute("SELECT position FROM Questions WHERE id = ?", (question.id,))
        current_position = cur.fetchone()[0]

        if current_position != question.position:
            # Ensure non-discontinuity by shifting positions
            if current_position < question.position:
                cur.execute(
                    "UPDATE Questions SET position = position - 1 WHERE position > ? AND position <= ?",
                    (current_position, question.position)
                )
            else:
                cur.execute(
                    "UPDATE Questions SET position = position + 1 WHERE position < ? AND position >= ?",
                    (current_position, question.position)
                )

        # Update the question with new details
        cur.execute(
            "UPDATE Questions SET title = ?, text = ?, image = ?, position = ? WHERE id = ?",
            (question.title, question.text, question.image, question.position, question.id)
        )
        conn.commit()

        # Update possible answers
        delete_answers_for_question(question.id)
        for answer in question.possibleAnswers:
            insert_answer(answer, question.id)