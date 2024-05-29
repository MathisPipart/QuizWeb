from flask import Flask, Response, request
from flask_cors import CORS

import hashlib
import sqlite3

import jwt_utils as ju
from converters import JSONToQuestion, questionToJSON
import database_utils as dbu

# Temporary password is 'flask2023'

app = Flask(__name__)
CORS(app)

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    sentPassword = payload['password'].encode('utf-8')
    hashedPassword = hashlib.md5(sentPassword).digest()
    
    if (hashedPassword != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'):
        return {"message": "Wrong password"}, 401
    else:
        token = ju.build_token()
        return {"token": token}, 200
    
@app.route('/questions', methods=['POST'])
def PostQuestion():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401

    question = JSONToQuestion(request.get_json())
    
    return {"id": dbu.insert_question(question)}, 200

@app.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    dbu.clear_questions()
    
    return Response(status=204)

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    if dbu.does_question_exist(question_id) is False:
        return {"message": "Question not found"}, 404
    
    dbu.delete_question(question_id)
    
    return Response(status=204)

@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestion(question_id):
    question = dbu.get_question(question_id)
    if question is None:
        return {"message": "Question not found"}, 404
    
    return questionToJSON(question), 200

@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
    position = request.args.get('position')
    if position is None:
        return {"message": "Position not provided"}, 400
    question = dbu.get_question_by_position(position)
    if question is None:
        return {"message": "Question not found"}, 404
    
    return questionToJSON(question), 200

@app.route('/questions/<int:question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    question = JSONToQuestion(request.get_json())
    question.id = question_id
    
    if dbu.does_question_exist(question_id) is False:
        return {"message": "Question not found"}, 404
    
    dbu.update_question(question)
    
    return Response(status=204)


if __name__ == '__main__':
    app.run()