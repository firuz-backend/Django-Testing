from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTestCase(TestCase):
    CREATED_NOTES_NUMBER = 10
    routes = {
        'edit': 'notes:edit',
        'detail': 'notes:detail',
        'delete': 'notes:delete',
        'home': reverse('notes:home'),
        'add': reverse('notes:add'),
        'list': reverse('notes:list'),
        'success': reverse('notes:success'),
        'login': reverse('users:login'),
        'logout': reverse('users:logout'),
        'signup': reverse('users:signup'),
    }

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Aziza')
        cls.reader = User.objects.create(username='Reader')

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.form_data = {
            'title': 'Note 1',
            'text': 'It is text',
            'slug': 'slug_ab1',
        }

        cls.note_add_url = cls.routes['add']


class BaseLogicTestCase(BaseTestCase):
    NOTE_TEXT = 'It is text'
    NEW_NOTE_TEXT = 'It is new note TEXT'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.note = Note.objects.create(
            title=cls.form_data['title'],
            text=cls.form_data['text'],
            slug=cls.form_data['slug'],
            author=cls.author,
        )

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
