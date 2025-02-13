from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import BaseTestCase, MixinTestCase


class NoteCreation(BaseTestCase):

    def test_anonymous_user_cant_create_note(self):
        note_count = Note.objects.count()
        response = self.client.post(self.note_add_url, data=self.form_data)
        login_url = self.routes['login']
        self.redirect_url = f'{login_url}?next={self.note_add_url}'
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Note.objects.count(), note_count)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            self.note_add_url, data=self.form_data
        )
        self.assertRedirects(response, self.routes['success'])

        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)


class TestNotetEditDelete(MixinTestCase):
    NOTE_TEXT = 'It is text'
    NEW_NOTE_TEXT = 'It is new note TEXT'

    def test_not_unique_slug(self):
        note_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.note_add_url, data=self.form_data)

        self.assertEqual(Note.objects.count(), note_count)
        self.assertFormError(
            response, form='form', field='slug',
            errors=(self.note.slug + WARNING))

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.note_add_url, data=self.form_data
        )

        self.assertRedirects(response, self.routes['success'])
        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get()
        expected_slug = slugify(note.title)
        self.assertEqual(note.slug, expected_slug)

    def test_author_can_edit_note(self):
        self.form_data['text'] = self.NEW_NOTE_TEXT
        response = self.author_client.post(
            self.routes['edit'], data=self.form_data)
        self.assertRedirects(response, self.routes['success'])

        refreshed_note = Note.objects.get(pk=self.note.id)

        self.assertEqual(refreshed_note.text, self.form_data['text'])
        self.assertEqual(refreshed_note.title, self.form_data['title'])
        self.assertEqual(refreshed_note.slug, self.form_data['slug'])
        self.assertEqual(refreshed_note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        self.form_data['text'] = self.NEW_NOTE_TEXT
        response = self.reader_client.post(
            self.routes['edit'], data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        refreshed_note = Note.objects.get(pk=self.note.id)

        self.assertEqual(refreshed_note.text, self.note.text)
        self.assertEqual(refreshed_note.title, self.note.title)
        self.assertEqual(refreshed_note.slug, self.note.slug)
        self.assertEqual(refreshed_note.author, self.note.author)

    def test_author_can_delete_note(self):
        note_count = Note.objects.count()
        response = self.author_client.delete(self.routes['delete'])
        self.assertRedirects(response, self.routes['success'])
        self.assertEqual(Note.objects.count(), note_count - 1)

    def test_user_cant_delete_another_note(self):
        note_count_expected = Note.objects.count()
        response = self.reader_client.delete(self.routes['delete'])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_expected)
