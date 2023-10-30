from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Bookmark, db
from flasgger import swag_from
import os
import uuid

sim = Blueprint("sim", __name__, url_prefix="/api/v1/sim")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads'  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@sim.route('/classify', methods=['POST'])
def similarity():
    country = request.args.get('country')
    type = request.args.get('type')
    print(f'{country} {type}')
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected image'}), HTTP_204_NO_CONTENT

    if file and allowed_file(file.filename):
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

        filename = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filename)

        # Itt hívd meg az osztályozó függvényt vagy modellt a képpel

        # Példa válasz visszatérítése
        result = {'classification': 'Cat', 'confidence': 0.98}, HTTP_200_OK
        return jsonify(result)
    else:
        return jsonify({'error': 'error in image processing'}), HTTP_500_INTERNAL_SERVER_ERROR