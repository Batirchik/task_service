import os

from flask import Flask
from flask import abort, request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from cache import c
from tasks import storing_data_to_file


# initialization
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from models import *


@auth.verify_password
def verify_password(username, password):
    # first try to authenticate by token
    token = request.args.get('token')
    if token:
        user = User.verify_auth_token(token)
    else:
        user = User.verify_auth_token(username)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# ============================================================================
@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.authorization.get('username')
    password = request.authorization.get('password')
    if not username or not password:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(409)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    g.user = user
    token = g.user.generate_auth_token(300)
    return (jsonify({'username': user.username,
                     'token': token.decode('ascii'),
                     'duration': 300}), 201)


@app.route('/apitoken')
@auth.login_required
def get_apitoken():
    token = g.user.generate_auth_token(300)
    return jsonify({'token': token.decode('ascii'),
                    'duration': 300})


@app.route('/task')
@auth.login_required
def get_task():
    key = 'task_success'
    task_exist = c.get_data(key)
    if task_exist:
        return '', 200
    abort(404)


@app.route('/task/start')
@auth.login_required
def start_task():
    key = 'task_success'
    task_exist = c.get_data(key)
    if task_exist:
        return 'Task has being started.'
    storing_data_to_file.apply_async()
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
