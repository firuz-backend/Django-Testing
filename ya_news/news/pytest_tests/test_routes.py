from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, args',
    (
        ('home', None),
        ('news_detail', lambda news: [news.id]),
        ('login', None),
        ('logout', None),
        ('signup', None),
    )
)
def test_pages_availability(client, news, name, args, routes):
    url = reverse(routes[name], args=args(news) if callable(args) else args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        ('news_edit', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        ('news_delete', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        ('news_edit', pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
        ('news_delete', pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
    )
)
def test_availbility_for_comment_edit_and_delete(
    name, parametrized_client, expected_status, comment, routes
):
    url = reverse(routes[name], args=(comment.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news_edit', 'news_delete')
)
def test_redirect_for_anonymous_client(client, name, comment, routes):
    login_url = reverse(routes['login'])
    url = reverse(routes[name], args=(comment.pk,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)

    assertRedirects(response, redirect_url)
