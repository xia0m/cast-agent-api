import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


from models import setup_db, db, Movie, Actor
from routes.movie import movie_routes
from routes.actor import actor_routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    movie_routes(app)
    actor_routes(app)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
