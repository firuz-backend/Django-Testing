from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

from .base import BaseTestCase

User = get_user_model()


class TestAuthorizedPages(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_create_and_update_page_has_form(self):

        urls = (
            (self.routes['add'], None),
            (self.routes['edit'], (self.note.slug, ))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = name if not args else reverse(name, args=args)
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
