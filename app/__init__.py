"""Application factory for the phishing detection project."""

from flask import Flask

from app.config import get_config
from app.db.database import close_db, init_app as init_db_app
from app.routes import main_bp


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    # Ensure Flask's instance directory exists for the SQLite database file.
    app.instance_path and __import__("os").makedirs(app.instance_path, exist_ok=True)

    init_db_app(app)
    app.teardown_appcontext(close_db)
    app.register_blueprint(main_bp)

    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    """Attach shared application-level error handlers."""

    @app.errorhandler(404)
    def not_found(_error):
        return (
            {"error": "The requested resource was not found."}
            if _wants_json()
            else (app.jinja_env.get_template("error.html").render(message="Page not found."), 404)
        )

    @app.errorhandler(500)
    def internal_error(_error):
        return (
            {"error": "An unexpected server error occurred."}
            if _wants_json()
            else (
                app.jinja_env.get_template("error.html").render(
                    message="An unexpected server error occurred."
                ),
                500,
            )
        )


def _wants_json() -> bool:
    """Return True when the current request prefers JSON over HTML."""
    from flask import request

    return request.accept_mimetypes.best == "application/json"
