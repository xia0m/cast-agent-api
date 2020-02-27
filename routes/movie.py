from models import Movie, db
from flask import abort, jsonify, request
from sqlalchemy.exc import IntegrityError


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

    @app.route('/movies', methods=['POST'])
    def create_movie():

        body = request.get_json()
        new_title = body.get('title', None)
        new_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title, release_date=new_date)
            db.session.add(movie)
            db.session.commit()

            movies = Movie.query.all()
            formated_movies = [movie.general_info() for movie in movies]
            return jsonify({
                'success': True,
                'total_movies': len(movies),
                'movies': formated_movies
            })
        except IntegrityError:
            db.session.rollback()
            print('Duplicated title name')
            abort(422)
        except BaseException:
            db.session.rollback()
            abort(422)

    """
    Update a movie entry by movie id
    """
    @app.route('/movies/<id>', methods=['PATCH'])
    def update_movie(id):
        # check wheter movie is in database, if not, return 404
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()

        for key, value in body.items():
            setattr(movie, key, value)

        try:
            db.session.commit()

            movies = Movie.query.all()
            formated_movies = [movie.general_info() for movie in movies]
            return jsonify({
                'success': True,
                'updated_movie_id': id,
                'movies': formated_movies
            })
        except IntegrityError:
            db.session.rollback()
            print('Duplicated title name')
            abort(422)
        except BaseException:
            db.session.rollback()
            abort(422)
