from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .base import MixinTestCase


User = get_user_model()


class TestRoutes(MixinTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_page_availabality_for_anonymous_user(self):
        urls = (
            self.routes['home'],
            self.routes['login'],
            self.routes['logout'],
            self.routes['signup'],
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_owner_and_no_owner_user(self):
        """
        The Test is for checking editing, deleting and
        detail show for ownerof note and no owner
        """
        user_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND)
        )

        for user, status in user_statuses:
            for name in (
                self.routes['edit'],
                self.routes['detail'],
                self.routes['delete']
            ):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_authorized_user(self):
        users = (
            self.author_client,
            self.reader_client
        )
        for user in users:
            for url in (
                self.routes['add'],
                self.routes['list'],
                self.routes['success']
            ):
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        SLUG = (self.note.slug, )
        urls = (
            (self.routes['add'], None),
            (self.routes['edit'], SLUG),
            (self.routes['detail'], SLUG),
            (self.routes['delete'], SLUG),
            (self.routes['list'], None),
            (self.routes['success'], None)
        )

        for name, args in urls:
            login_url = reverse('users:login')
            with self.subTest(name=name):
                url = name if not args else reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
