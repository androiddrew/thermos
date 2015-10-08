from thermos import app, db
from thermos.models import User
from flask.ext.script import Manager, prompt_bool


manager = Manager(app)

@manager.command
def initdb():
	db.create_all()
	db.session.add(User(username="AndroidDrew", email="androiddrew@gmail.com", password="test"))
	db.session.add(User(username="LauraKolady", email="LauraKolday@gmail.com", password="test"))
	db.session.commit()
	print("Initialized the database")

@manager.command
def dropdb():
	if prompt_bool("Are you sure you want to delete the db?"):
		db.drop_all()
		print("Dropped the database")

if __name__ == '__main__':
	manager.run() 