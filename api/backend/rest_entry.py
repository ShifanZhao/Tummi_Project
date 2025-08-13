from flask.json.provider import DefaultJSONProvider
from datetime import date, datetime, timedelta
from decimal import Decimal #Ray Trying to Fix Json-Interpreting-Time Problem
from flask import Flask
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.db_connection import db
from backend.simple.simple_routes import simple_routes
from backend.ngos.ngo_routes import ngos
from backend.Restaurant_Owners.RestOwner_routes import restowners
from backend.Casual_Diner.CasualDiner_routes import casualdiner
from backend.Internal_Analyst.Internal_Analyst_routes import internal
from backend.Food_Influencer.food_influencer_routes import foodinfluencer

##Ray Time Problem 
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, timedelta):
            total = int(o.total_seconds())
            h, m, s = total // 3600, (total % 3600) // 60, total % 60
            return f"{h:02d}:{m:02d}:{s:02d}"
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

def create_app():
    ##Ray Time
    # 使用自定义 JSON Provider（解决 timedelta / datetime / Decimal 等序列化）
    app = Flask(__name__)
    app.json_provider_class = CustomJSONProvider
    app.json = app.json_provider_class(app)
    

    # Configure logging
    # Create logs directory if it doesn't exist
    setup_logging(app)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # # these are for the DB object to be able to connect to MySQL.
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv(
        "DB_NAME"
    ).strip()  # Change this to your DB name

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info("create_app(): registering blueprints with Flask app object.")
    app.register_blueprint(simple_routes)
    app.register_blueprint(ngos, url_prefix="/ngo")
    app.register_blueprint(restowners, url_prefix="/ro")
    app.register_blueprint(casualdiner, url_prefix="/cd")
    app.register_blueprint(internal, url_prefix="/ita")
    app.register_blueprint(foodinfluencer, url_prefix="/fi")

    # Don't forget to return the app object
    return app

def setup_logging(app):
    """
    Configure logging for the Flask application in both files and console (Docker Desktop for this project)
    
    Args:
        app: Flask application instance to configure logging for
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    ## Set up FILE HANDLER for all levels
    file_handler = RotatingFileHandler(
        'logs/api.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    # Make sure we are capturing all levels of logging into the log files. 
    file_handler.setLevel(logging.DEBUG)  # Capture all levels in file
    app.logger.addHandler(file_handler)

    ## Set up CONSOLE HANDLER for all levels
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    # Debug level capture makes sure that all log levels are captured
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    # Set the base logging level to DEBUG to capture everything
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')