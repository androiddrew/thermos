from thermos import app, db
from thermos.models import User, Bookmark, Tag
from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    androiddrew = User(username="AndroidDrew", email="androiddrew@gmail.com", password="test")

    db.session.add(androiddrew)
    db.session.add(User(username="LauraKolady", email="LauraKolday@gmail.com", password="test"))

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description, user=androiddrew,
                                tags=tags))

    for name in ["python", "flask", "webdev", "programming", "training", "news", "orm", "database",
                 "social", "bookmarking"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark('http://www.reddit.com', 'A better social bookmarking site', "news, social, bookmarking")
    add_bookmark('http://www.hackaday.com', 'The DIY hacking blog you have to read', "news, social, programming")
    db.session.commit()


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to delete the db?"):
        db.drop_all()
        print("Dropped the database")


if __name__ == '__main__':
    manager.run()
