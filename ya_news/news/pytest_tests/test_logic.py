from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


COMMENT_DATA = {'text': 'Текст комментария'}


def test_anonymous_user_cant_create_comment(
    client, news, routes
):
    comment_count = Comment.objects.count()
    url = reverse(routes['news_detail'], args=(news.pk,))
    response = client.post(url, COMMENT_DATA)

    login_url = reverse(routes['login'])
    expected_url = f'{login_url}?next={url}'

    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_count


def test_user_can_create_comment(
    author_client, news, author, routes
):
    Comment.objects.all().delete()
    url = reverse(routes['news_detail'], args=(news.pk,))
    response = author_client.post(url, COMMENT_DATA)

    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == COMMENT_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news, routes):
    url = reverse(routes['news_detail'], args=(news.pk,))
    comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, bad_words_data)

    assertFormError(response, 'form', 'text', WARNING)
    assert Comment.objects.count() == comment_count


def test_author_can_delete_comment(author_client, comment, news, routes):
    url = reverse(routes['news_delete'], args=(comment.pk,))
    response = author_client.delete(url)

    url_to_comments = reverse(routes['news_detail'], args=(news.id,))
    url_to_comments = f'{url_to_comments}#comments'
    assertRedirects(response, url_to_comments)

    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, routes
):
    url = reverse(routes['news_delete'], args=(comment.pk,))
    response = not_author_client.delete(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    author, author_client, comment, news, routes
):
    url = reverse(routes['news_edit'], args=(comment.pk,))
    data = {'text': 'It is edited comment'}

    response = author_client.post(url, data)
    edited_comment = Comment.objects.get(id=comment.id)

    assert edited_comment.news == news
    assert edited_comment.author == author

    url_to_comments = reverse(routes['news_detail'], args=(news.pk,))
    url_to_comments = f'{url_to_comments}#comments'

    assertRedirects(response, url_to_comments)
    assert edited_comment.text == data['text']


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, routes
):
    url = reverse(routes['news_edit'], args=(comment.pk,))
    data = {'text': 'It is edited comment'}
    response = not_author_client.post(url, data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    fetched_comment = Comment.objects.get(id=comment.id)

    assert fetched_comment.text == comment.text
    assert fetched_comment.author == comment.author
    assert fetched_comment.news == comment.news
