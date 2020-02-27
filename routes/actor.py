from models import Actor
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
