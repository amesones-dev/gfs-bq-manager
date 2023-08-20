from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

# To implement Google Cloud BigQuery
from gbq_manager import GBQManager
from gbq_content_manager import AppBQContentManager

# Basic Big Query sourced data in memory content manager
# Loads data from BQ using a preconfigured set
# Basic management of content freshness
# to avoid running BigQuery sql queries
# Improvement: adding content cache service (redis, memcache)


bootstrap = Bootstrap()
bq = GBQManager()
app_bq_cm = AppBQContentManager()


def create_app(config_class=Config):
    # Create Flask app
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_class)

    # Initialize Bootstrap (HTML, CSS, JS)  manager
    bootstrap.init_app(app)

    # Initialize BigQuery connection manager
    bq.init_app(app)

    # Initialize BigQuery Content Manager
    app_bq_cm.init_app(app, bq=bq)

    # Flask blueprints imports
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    if not app.debug and not app.testing:
        # Extra initialization when testing or debugging
        pass

    return app
