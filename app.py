from flask import Flask

from config import Config
from models.database import init_app, initialize_database
from controllers.public_controller import public_bp
from controllers.admin_controller import admin_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    init_app(app)
    with app.app_context():
        initialize_database()

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
