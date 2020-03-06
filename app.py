import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


from models import setup_db, db
from routes import setup_routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    setup_routes(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
