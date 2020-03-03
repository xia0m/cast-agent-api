from .movie import movie_routes
from .actor import actor_routes
from .error import error_routes


def setup_routes(app):
    movie_routes(app)
    actor_routes(app)
    error_routes(app)
