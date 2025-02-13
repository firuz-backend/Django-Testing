from http import HTTPStatus

from .base import MixinTestCase


class TestRoutes(MixinTestCase):

    def test_page_availabality_for_anonymous_user(self):
        urls = ('home', 'login', 'logout', 'signup')

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(self.routes[url])
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
            for url in ('edit', 'detail', 'delete'):
                url = self.routes[url]
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_authorized_user(self):
        users = (
            self.author_client,
            self.reader_client
        )
        for user in users:
            for url in ('add', 'list', 'success'):
                url = self.routes[url]
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        urls = ('add', 'edit', 'detail', 'delete', 'list', 'success')

        for url in urls:
            login_url = self.routes['login']
            url = self.routes[url]
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
