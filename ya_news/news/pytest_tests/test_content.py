from django.conf import settings
from django.urls import reverse
import pytest

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(client, news_batch, routes):
    url = reverse(routes['home'])
    response = client.get(url)

    assert (
        response.context['object_list'].count()
        == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_ten_news_order(news_batch, client, routes):
    url = reverse(routes['home'])
    response = client.get(url)

    news = response.context['object_list']
    all_date = [item.date for item in news]
    sorted_dates = sorted(all_date, reverse=True)

    assert all_date == sorted_dates


def test_ten_comment_order(client, ten_comments, news, routes):
    url = reverse(routes['news_detail'], args=(news.pk, ))
    response = client.get(url)

    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)

    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, news, routes):
    url = reverse(routes['news_detail'], args=(news.pk,))
    response = client.get(url)

    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, routes):
    url = reverse(routes['news_detail'], args=(news.pk,))
    response = author_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
