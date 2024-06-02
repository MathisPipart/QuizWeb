from flask import Flask
from flask_cors import CORS
from routes.quiz_routes import quiz_bp
from routes.admin_routes import admin_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from database.admin_db import init_db
init_db()

CORS(app)

app.register_blueprint(quiz_bp, url_prefix='')
app.register_blueprint(admin_bp, url_prefix='')

if __name__ == '__main__':
    app.run(debug=True)
