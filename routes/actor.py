from models import Actor, Movie, db
from flask import abort, jsonify, request


def actor_routes(app):

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

    @app.route('/actors/<id>', methods=['GET'])
    def retrieve_actor_by_id(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    """
    Post a new actor
    """

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', 0)
        new_gender = body.get('gender', None)
        new_movie_id = body.get('movie_id', 0)

        try:
            # check whether the movie exist
            movie = Movie.query.filter(Movie.id == new_movie_id).one_or_none()
            if movie is None:
                print('No movie found with given movie id')
                abort(400)

            actor = Actor(name=new_name, age=new_age,
                          gender=new_gender, movie_id=new_movie_id)
            db.session.add(actor)
            db.session.commit()

            actors = Actor.query.all()
            formated_actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'total_actors': len(actors),
                'actors': formated_actors
            })
        except IntegrityError:
            db.session.rollback()
            print('Duplicated actor name')
            abort(422)
        except BaseException:
            db.session.rollback()
            abort(422)
    """
    Update a actor entry based on id

    """
    @app.route('/actors/<id>', methods=['PATCH'])
    def update_actor(id):
        # check wheter movie is in database, if not, return 404
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()

        # update only what attribute body has
        for key, value in body.items():
            setattr(actor, key, value)

        try:
            db.session.commit()

            actors = Actor.query.all()
            formated_actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'updated_actor_id': id,
                'actors': formated_actors
            })
        except IntegrityError:
            db.session.rollback()
            print('Duplicated title name')
            abort(422)
        except BaseException:
            db.session.rollback()
            abort(422)

    """
    Delete actor based on id
    """
    @app.route('/actors/<id>', methods=['DELETE'])
    def delete_actor(id):
        # check wheter movie is in database, if not, return 404
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)

        try:
            db.session.delete(actor)
            db.session.commit()

            actors = Actor.query.all()
            formated_actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'deleted': id,
                'actors': formated_actors
            })
        except BaseException:
            db.session.rollback()
            abort(422)
