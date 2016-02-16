from flask_testing import TestCase

import thermos
from thermos.models import User

class ThermosTestBase(TestCase):

    def create_app(self):
        return thermos.create_app('test')


    def setUp(self):
        thermos.admin._views = [] #Workaround for blueprint registration
        #rest_api.resources = [] #Workaround for blueprint registration
        self.db = thermos.db
        with self.app.app_context():
            self.db.create_all()
        self.client = self.app.test_client()

        self.test_user = User(username='test', email='fake@email.com', password='test')

        self.db.session.add(self.test_user)
        self.db.session.commit()

    def tearDown(self):
        thermos.db.session.remove()
        thermos.db.drop_all()