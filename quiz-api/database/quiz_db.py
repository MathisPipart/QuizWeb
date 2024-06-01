import sqlite3
from config import Config
from utils.classes import Question, Answer

# Get the quiz info (size and previous scores)
def get_quiz_info():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
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

# Gets all answers for a question
def get_answers(question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Answers WHERE questionId = ?", (question_id,))
        answers = cur.fetchall()
        
        return [Answer(text = answer[1], isCorrect = answer[2]) for answer in answers]
    
    # Gets all questions from the database
def get_questions():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions")
        questions = cur.fetchall()
        
        return [Question(title = question[2], text = question[3], image = question[4], position = question[1], possibleAnswers = get_answers(question[0])) for question in questions]
    
# Gets a question from the database
def get_question(question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE id = ?", (question_id,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
# Gets a question from the database by position
def get_question_by_position(position):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Questions WHERE position = ?", (position,))
        question = cur.fetchone()
        
        if question is None:
            return None
        
        return Question(title = question[2], text = question[3], image = question[4], position = question[1], id = question[0], possibleAnswers = get_answers(question[0]))
    
# Checks if a question exists in the database  
def does_question_exist(question_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Questions WHERE id = ?", (question_id,))
        return cur.fetchone()[0] > 0
    
# Inserts a participation into the database
def insert_participation(playerName, answers):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
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