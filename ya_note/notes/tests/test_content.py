from notes.forms import NoteForm
from .base import MixinTestCase


class TestAuthorizedPages(MixinTestCase):

    def test_create_and_update_page_has_form(self):

        urls = (
            'add',
            'edit'
        )
        for url in urls:
            url = self.routes[url]
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_for_different_users(self):
        users_and_status = (
            (self.author_client, True),
            (self.reader_client, False)
        )

        url = self.routes['list']
        for user, status in users_and_status:
            with self.subTest(user=user):
                response = user.get(url)
                notes = response.context['object_list']
                self.assertEqual(self.note in notes, status)
