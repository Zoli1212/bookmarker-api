from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register', methods=['POST'])
def register():
    return 'User created successfully'

@auth.route('/me', methods=['GET'])
def me():
    return {'user': 'me'}
