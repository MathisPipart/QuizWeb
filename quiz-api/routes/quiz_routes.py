from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
import database.quiz_db as quiz_db
from utils.converters import questionToJSON, JSONToQuestion

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return quiz_db.get_quiz_info(), 200

@quiz_bp.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestion(question_id):
	question = quiz_db.get_question(question_id)
	if question is None:
		return {"message": "Question not found"}, 404
		
	return questionToJSON(question), 200

@quiz_bp.route('/questions', methods=['GET'])
def GetQuestionByPosition():
	position = request.args.get('position')
	if position is None:
		return {"message": "Position not provided"}, 400
	question = quiz_db.get_question_by_position(position)
	if question is None:
		return {"message": "Question not found"}, 404
		
	return questionToJSON(question), 200

@quiz_bp.route('/participations', methods=['POST', 'OPTIONS'])
@cross_origin()
def PostParticipation():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
        
    payload = request.get_json()
    playerName = payload['playerName']
    answers = payload['answers']
        
    result = quiz_db.insert_participation(playerName, answers)
    
    # If the insertion returns an error message with a status code, handle it accordingly
    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], int):
        return jsonify(result[0]), result[1]
    
    return jsonify(result), 200

def _build_cors_preflight_response():
    response = Response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response