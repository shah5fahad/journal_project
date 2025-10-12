from main_app.models import db
from main_app.routes import app
from flask_migrate import Migrate

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)