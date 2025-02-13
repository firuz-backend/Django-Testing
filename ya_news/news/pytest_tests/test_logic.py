from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


COMMENT_DATA = {'text': 'Текст комментария'}
EDITED_COMMENT_DATA = {'text': 'It is edited comment'}


def test_anonymous_user_cant_create_comment(
    client, news, routes
):
    comment_count = Comment.objects.count()
    url = routes['news_detail']
    response = client.post(url, COMMENT_DATA)

    login_url = routes['login']
    expected_url = f'{login_url}?next={url}'

    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_count


def test_user_can_create_comment(
    author_client, news, author, routes
):
    Comment.objects.all().delete()
    url = routes['news_detail']
    response = author_client.post(url, COMMENT_DATA)

    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == COMMENT_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news, routes):
    url = routes['news_detail']
    comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, bad_words_data)

    assert Comment.objects.count() == comment_count
    assertFormError(response, 'form', 'text', WARNING)


def test_author_can_delete_comment(author_client, comment, news, routes):
    comment_count = Comment.objects.count()

    url = routes['news_delete']
    response = author_client.delete(url)

    url_to_comments = routes['news_detail']
    url_to_comments = f'{url_to_comments}#comments'
    assertRedirects(response, url_to_comments)

    assert Comment.objects.count() == comment_count - 1


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, routes
):
    url = routes['news_delete']
    response = not_author_client.delete(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    author, author_client, comment, news, routes
):
    url = routes['news_edit']

    response = author_client.post(url, EDITED_COMMENT_DATA)
    edited_comment = Comment.objects.get(id=comment.id)

    assert edited_comment.news == comment.news
    assert edited_comment.author == comment.author

    url_to_comments = routes['news_detail']
    url_to_comments = f'{url_to_comments}#comments'

    assertRedirects(response, url_to_comments)
    assert edited_comment.text == EDITED_COMMENT_DATA['text']


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, routes
):
    url = routes['news_edit']
    response = not_author_client.post(url, data=EDITED_COMMENT_DATA)

    assert response.status_code == HTTPStatus.NOT_FOUND

    fetched_comment = Comment.objects.get(id=comment.id)

    assert fetched_comment.text == comment.text
    assert fetched_comment.author == comment.author
    assert fetched_comment.news == comment.news
