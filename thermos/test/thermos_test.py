from flask import url_for
from flask_testing import TestCase

import thermos
from thermos.models import User, Bookmark

class ThermosTestCase(TestCase):

    def create_app(self):
        return thermos.create_app('test')

    def setUp(self):
        self.db = thermos.db
        with self.app.app_context():
            self.db.create_all()
        self.client = self.app.test_client()

        u = User(username='test', email='fake@email.com', password='test')
        bm = Bookmark(user=u, url='http://hackaday.com', description='A DIY hacking blog', tags='one,two,three')

        self.db.session.add(u)
        self.db.session.add(bm)
        self.db.session.commit()

        #get the cookie!
        self.client.post(url_for('auth.login'),
                         data=dict(username='test', password='test'))

    def tearDown(self):
        thermos.db.session.remove()
        thermos.db.drop_all()

    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('bookmarks.edit_bookmark', bookmark_id=1),
            data = dict(url='http://hackaday.com',
                        tags=""
            ),
            follow_redirects = True
        )

        assert response.status_code == 200
        bm = Bookmark.query.first()
        assert not bm._tags