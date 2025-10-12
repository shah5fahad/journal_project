import os
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()
mail = Mail()


# flask --app run.py db init
# flask --app run.py db migrate -m "Message"
# flask --app run.py db upgrade
# rever migrations
# flask --app run.py db downgrade

def init_config():
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS").lower() == "true"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)

# Init database
init_config()