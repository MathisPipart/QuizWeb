import sqlite3
import classes

databaseFile = 'db.db'


# Rebuilds the database, dropping all tables and recreating them
def rebuild_db():
    with sqlite3.connect(databaseFile) as conn:
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
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        # Find the maximum position
        cur.execute("SELECT MAX(position) FROM Questions")
        max_position = cur.fetchone()[0]
        max_position = max_position if max_position is not None else 0

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
    with sqlite3.connect(databaseFile) as conn:
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
    with sqlite3.connect(databaseFile) as conn:
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
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE id = ?", (answer_id,))
        conn.commit()
       
# Deletes all answers for a question 
def delete_answers_for_question(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers WHERE questionId = ?", (question_id,))
        conn.commit()
   
# Deletes all questions from the database 
def clear_questions():
    clear_answers()
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Questions")
        conn.commit()
       
# Deletes all answers from the database 
def clear_answers():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Answers")
        conn.commit()
        
# Deletes all participations from the database
def clear_participations():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("DELETE FROM Participations")
        conn.commit()
       
# Gets all answers for a question
def get_answers(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Answers WHERE questionId = ?", (question_id,))
        answers = cur.fetchall()
        
        return [classes.Answer(text = answer[1], isCorrect = answer[2]) for answer in answers]
        
# Gets all questions from the database
def get_questions():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions")
        questions = cur.fetchall()
        
        return [classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], possibleAnswers = get_answers(question[0])) for question in questions]
    
# Gets a question from the database
def get_question(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE id = ?", (question_id,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
# Gets a question from the database by position
def get_question_by_position(position):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE position = ?", (position,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return classes.Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
# Updates a question in the database
def update_question(question):
    with sqlite3.connect(databaseFile) as conn:
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
          
# Checks if a question exists in the database  
def does_question_exist(question_id):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Questions WHERE id = ?", (question_id,))
        return cur.fetchone()[0] > 0
    
# Get the quiz info (size and previous scores)
def get_quiz_info():
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Questions")
        question_count = cur.fetchone()[0]
        
        # Fetch participations sorted by score
        cur.execute("SELECT * FROM Participations ORDER BY score DESC")
        participations = cur.fetchall()
        
        return {
            "size": question_count,
            "scores": [{"playerName": participant[1], "score": participant[2]} for participant in participations]
        }

# Inserts a participation into the database
def insert_participation(playerName, answers):
    with sqlite3.connect(databaseFile) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        score = 0
        
        # Fetch all questions sorted by their position
        cur.execute("SELECT * FROM Questions ORDER BY position")
        questions = cur.fetchall()
        question_count = len(questions)
        
        # Check if the number of answers matches the number of questions
        if len(answers) != question_count:
            return {"message": "Bad request"}, 400
        
        for i in range(question_count):
            question_id = questions[i][0]
            # Fetch possible answers for the current question
            cur.execute("SELECT * FROM Answers WHERE questionId = ?", (question_id,))
            possible_answers = cur.fetchall()
            
            for j in range(len(possible_answers)):
                if answers[i] == j + 1 and possible_answers[j][2] == 1:
                    score += 1
                    break
        
        # Insert the participation into the database
        cur.execute("INSERT INTO Participations (playerName, score) VALUES (?, ?)", (playerName, score))
        conn.commit()

        return {"playerName": playerName, "score": score}