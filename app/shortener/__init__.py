"""App factory"""
from flask import Flask
from flask_json import FlaskJSON
from .models.model import db, Link
from .views import page


def create_app():
    """App factory"""
    app = Flask(__name__)
    app.register_blueprint(page)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'

    @app.cli.command("create-database")
    def create_database(): # pylint: disable=unused-variable
        db.create_all(app=app)

    @app.cli.command("purge-database")
    def purge_database(): # pylint: disable=unused-variable
        for entry in Link.query.all():
            db.session.delete(entry)
        db.session.commit()
        print(len(Link.query.all()))

    db.init_app(app)
    FlaskJSON(app)
    return app
