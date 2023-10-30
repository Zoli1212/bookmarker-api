# __init__.py

from flask import Flask, config, redirect
from flask.json import jsonify
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db
from src.compute import sim
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.database import db, Bookmark
from src.config.swagger import template, swagger_config

from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATION=False,
            JWT_SECRET_KE=os.environ.get('JWT_SECRET_KEY'),
            UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

        )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)

    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app