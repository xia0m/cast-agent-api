from auth import AuthError
from flask import jsonify


def error_routes(app):
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(AuthError)
    def not_auth_error(e):
        error = getattr(e, 'error', None)
        status_code = getattr(e, 'status_code', None)

        return jsonify({
            'success': False,
            'code': error['code'],
            'description': error['description'],
        }), status_code
