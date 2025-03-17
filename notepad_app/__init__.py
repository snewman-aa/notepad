import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import humanize


db = SQLAlchemy()

def create_app():
    """Application factory function."""
    app = Flask(__name__, instance_relative_config=True)

    # Not deployed, so just using a simple secret key
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'notes.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    # Injecting notes into all templates so the sidebar can display them
    @app.context_processor
    def inject_notes():
        from notepad_app.models import Note  # See, Marc, no circular import
        notes = Note.query.order_by(Note.created_at.desc()).all()
        return dict(notes=notes)


    # Using humanize to make dates social-media vibes
    @app.template_filter('social_date')
    def social_date_filter(date_value):
        if not date_value:
            return ""

        now = datetime.datetime.now()
        time_difference = now - date_value

        if time_difference < datetime.timedelta(minutes=1):
            return "Just now"
        elif time_difference < datetime.timedelta(hours=1):
            return humanize.naturaltime(date_value)
        elif date_value.date() == now.date():
            return date_value.strftime("h:%ma")
        elif date_value.date() == (now - datetime.timedelta(days=1)).date():
            return "Yesterday"
        elif date_value.year == now.year:
            return date_value.strftime("%b %d")
        else:
            return date_value.strftime("%Y-%m-%d")

    with app.app_context():
        db.create_all()

    return app