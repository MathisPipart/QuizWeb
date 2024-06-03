from flask import Blueprint, request, Response
from flask_cors import cross_origin
import hashlib
import database.admin_db as admin_db
import database.quiz_db as quiz_db
import utils.jwt_utils as ju
from utils.converters import questionToJSON, JSONToQuestion

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def Login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    payload = request.get_json()
    sentPassword = payload['password'].encode('utf-8')
    hashedPassword = hashlib.md5(sentPassword).digest()
    
    if (hashedPassword != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'):
        return {"message": "Wrong password"}, 401
    else:
        token = ju.build_token()
        return {"token": token}, 200

@admin_bp.route('/rebuild-db', methods=['POST', 'OPTIONS'])
@cross_origin()
def RebuildDB():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.rebuild_db()
    
    return "Ok", 200

@admin_bp.route('/questions', methods=['POST', 'OPTIONS'])
@cross_origin()
def PostQuestion():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401

    question = JSONToQuestion(request.get_json())
    
    return {"id": admin_db.insert_question(question)}, 200

@admin_bp.route('/questions/<int:question_id>', methods=['PUT', 'OPTIONS'])
@cross_origin()
def UpdateQuestion(question_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    question = JSONToQuestion(request.get_json())
    question.id = question_id
    
    if quiz_db.does_question_exist(question_id) is False:
        return {"message": "Question not found"}, 404
    
    admin_db.update_question(question)
    
    return Response(status=204)

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def DeleteQuestion(question_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    if quiz_db.does_question_exist(question_id) is False:
        return {"message": "Question not found"}, 404
    
    admin_db.delete_question(question_id)
    
    return Response(status=204)

@admin_bp.route('/questions/all', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def DeleteAllQuestions():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.clear_questions()
    
    return Response(status=204)

@admin_bp.route('/participations/all', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def DeleteAllParticipations():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.clear_participations()
    
    return Response(status=204)

def _build_cors_preflight_response():
    response = Response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response
