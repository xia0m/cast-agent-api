import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


from models import setup_db, db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.route('/movies', methods=['GET'])
    def retrieve_movies():
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        formated_movies = [movie.general_info() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formated_movies
        })

    @app.route('/movies/<id>', methods=['GET'])
    def retrieve_movie_by_id(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.detailed_info()
        })

    @app.route('/actors', methods=['GET'])
    def retrieve_actors():
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        formated_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formated_actors
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
