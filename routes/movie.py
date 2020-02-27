from models import Movie
from flask import abort, jsonify, request


def movie_routes(app):

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
