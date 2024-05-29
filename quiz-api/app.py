from flask import Flask, request
from flask_cors import CORS

import hashlib
import jwt_utils

# Temporary password is 'password'

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    x = "world"
    return f'Hello, {x}!'

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    sentPassword = payload['password'].encode('utf-8')
    hashedPassword = hashlib.md5(sentPassword).digest()
    
    if (hashedPassword != b"_M\xcc;Z\xa7e\xd6\x1d\x83'\xde\xb8\x82\xcf\x99"):
        return {"message": "Wrong password"}, 401
    else:
        return {"token": jwt_utils.build_token()}, 200
    

if __name__ == '__main__':
    app.run()