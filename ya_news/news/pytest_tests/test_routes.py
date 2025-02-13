from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        ('home', lazy_fixture('client'), HTTPStatus.OK),
        ('news_detail', lazy_fixture('client'), HTTPStatus.OK),
        ('login', lazy_fixture('client'), HTTPStatus.OK),
        ('logout', lazy_fixture('client'), HTTPStatus.OK),
        ('signup', lazy_fixture('client'), HTTPStatus.OK),
        ('news_edit', lazy_fixture('author_client'), HTTPStatus.OK),
        ('news_delete', lazy_fixture('author_client'), HTTPStatus.OK),
        ('news_edit', lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        ('news_delete', lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(
    name, parametrized_client, expected_status, routes
):
    url = routes[name]

    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news_edit', 'news_delete')
)
def test_redirect_for_anonymous_client(client, name, comment, routes):
    login_url = routes['login']
    url = routes[name]
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)

    assertRedirects(response, redirect_url)
