from flask import url_for
from werkzeug.exceptions import HTTPException
import thermos
from . import ThermosTestBase
from thermos.models import User, Bookmark

class HompageTestCase(ThermosTestBase):

    def test_template_empty_db(self):
        response = self.client.get(url_for('main.index'))
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        assert b'No bookmarks have been added yet.' in response.data

    def test_bookmark_newest(self):
        with self.app.app_context():
            user = User.query.filter_by(username='test').first()
        self.db.session.add(Bookmark(user=user, url='http://hackaday.com', description='A DIY hacking blog', tags='one,two,three'))
        self.db.session.commit()
        response = self.client.get(url_for('main.index'))
        self.assertEqual(self.get_context_variable('new_bookmarks').count(), 1)

class AddBookmarkTestCase(ThermosTestBase):

    def test_add_login_required(self):
        response = self.client.get(url_for('bookmarks.add'), follow_redirects=False)
        #Want to pass the query string in the assertion check too
        self.assertRedirects(response,url_for('auth.login') + response.location[response.location.find('?'):])

    def test_add_bookmark(self):
        self.client.post(url_for('auth.login'),
                         data=dict(username='test', password='test'))
        response = self.client.post(url_for('bookmarks.add'),
                                     data=dict(url='hackaday.com', description='A lovely DIY site'),
                             follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertEqual(self.get_context_variable('new_bookmarks').count(), 1)
        bm = Bookmark.query.first()
        assert bm.user_id == 1
        assert bm.url == 'http://hackaday.com'

class EditBookmarkTestCase(ThermosTestBase):

    def setUp(self):
        thermos.admin._views = [] #Workaround for blueprint registration
        #rest_api.resources = [] #Workaround for blueprint registration
        self.db = thermos.db
        with self.app.app_context():
            self.db.create_all()
        self.client = self.app.test_client()

        self.test_user = User(username='test', email='fake@email.com', password='test')

        self.db.session.add(self.test_user)
        bm = Bookmark(user=self.test_user, url='http://hackaday.com', description='A DIY hacking blog', tags='one,two,three')
        self.db.session.add(bm)
        self.db.session.commit()

        other_user = User(username='test2', email='fake2@email.com', password='test')
        self.db.session.add(other_user)
        bm2 = Bookmark(user=other_user, url='http://phys.org', description='A phyics news site', tags='one,two,three')
        self.db.session.add(bm2)
        self.db.session.commit()

    def test_edit_login_required(self):
        response = self.client.get(url_for('bookmarks.edit_bookmark', bookmark_id=1), follow_redirects=False)
        #Want to pass the query string in the assertion check too
        self.assertRedirects(response,url_for('auth.login') + response.location[response.location.find('?'):])

    def test_delete_all_tags(self):
        self.client.post(url_for('auth.login'),
                         data=dict(username='test', password='test'))
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

    def test_edit_bookmark_not_found(self):
        self.client.post(url_for('auth.login'),
                         data=dict(username='test', password='test'))
        response = self.client.get(url_for('bookmarks.edit_bookmark', bookmark_id=3))
        self.assert_404(response)

    #NEED TO CHANGE THIS TO BY PASS THE APP ERROR HANDLER OR YOU JUST DON'T UNIT TEST THE ABORT object
    def test_edit_bookmark_incorrect_user(self):
        self.client.post(url_for('auth.login'),
                         data=dict(username='test2', password='test'))
        with self.assertRaises(HTTPException):
            self.client.get(url_for('bookmarks.edit_bookmark', bookmark_id=1), follow_redirects=False)
