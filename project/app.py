from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.db"
app.config["SECRET_KEY"] = "ajsdhqg837fgh3g283gcb236yrg3bunci37"
db = SQLAlchemy(app)
migrate = Migrate(app, db)