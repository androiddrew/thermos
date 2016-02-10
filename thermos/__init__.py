from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .config import config_by_name

db = SQLAlchemy()
admin = Admin(name='Thermos', template_mode='zurb5')

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


toolbar = DebugToolbarExtension()

# for displaying timestamps
moment = Moment()

def create_app(config_name):
    """Flask app creation factory"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    admin.init_app(app)

    from .models import Bookmark
    admin.add_view(ModelView(Bookmark, db.session))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .bookmarks import bookmarks as bookmarks_blueprint
    app.register_blueprint(bookmarks_blueprint, url_prefix='/bookmarks')


    return app



