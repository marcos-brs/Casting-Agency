from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=80, debug=True)
