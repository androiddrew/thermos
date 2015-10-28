from flask import render_template

from . import main
from .. import login_manager
from ..models import User, Bookmark, Tag


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html'), 404  # returns tuple that includes status code for the page failing to do so will prevent flask \
    # from setting the correct status code one the return


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500  # debug needs to be turned off to hit 500

@main.app_context_processor
def inject_tags():
    """Will return only a dict object that is made available to all templates. We used Tag.all to reference the function
     without calling the function. This will prevent the database from executing the all() query everytime we process
     a template. Instead we make the function available for calling in the individual template where it is needed."""
    return dict(all_tags=Tag.all)