from flask import Flask
from routes import create_api_blueprint
import logging


def create_flask_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    flask_app = Flask(__name__)

    # Register the API blueprint with the Flask application
    api_blueprint = create_api_blueprint()
    flask_app.register_blueprint(api_blueprint, url_prefix='/api')

    return flask_app


if __name__ == "__main__":
    # Configure logging for the entire application
    logging.basicConfig(level=logging.ERROR)

    # Create and run the Flask application
    app = create_flask_app()
    app.run(debug=True)