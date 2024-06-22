from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tax_filing_assistant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['OPENAI_API_KEY'] = 'fill OPENAI_API_KEY'  

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app
# sk-proj-zEF5cRDrB2jYNGPbs2DHT3BlbkFJ7b47wSMSLKaSxKuUs6jq

