from flask import Blueprint, request, Response
import hashlib
import database.admin_db as admin_db
import database.quiz_db as quiz_db
import utils.jwt_utils as ju
from utils.converters import questionToJSON, JSONToQuestion

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    sentPassword = payload['password'].encode('utf-8')
    hashedPassword = hashlib.md5(sentPassword).digest()
    
    if (hashedPassword != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'):
        return {"message": "Wrong password"}, 401
    else:
        token = ju.build_token()
        return {"token": token}, 200

@admin_bp.route('/rebuild-db', methods=['POST'])
def RebuildDB():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.rebuild_db()
    
    return "Ok", 200

@admin_bp.route('/questions', methods=['POST'])
def PostQuestion():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401

    question = JSONToQuestion(request.get_json())
    
    return {"id": admin_db.insert_question(question)}, 200

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
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

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    if quiz_db.does_question_exist(question_id) is False:
        return {"message": "Question not found"}, 404
    
    admin_db.delete_question(question_id)
    
    return Response(status=204)

@admin_bp.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.clear_questions()
    
    return Response(status=204)

@admin_bp.route('/participations/all', methods=['DELETE'])
def DeleteAllParticipations():
    try:
        ju.auth_midleware(request)
    except ju.JwtError as e:
        return {"message": str(e)}, 401
    
    admin_db.clear_participations()
    
    return Response(status=204)