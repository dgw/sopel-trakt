from __future__ import annotations

import pytest
import unittest.mock

from sopel_trakt import errors, util


def test_get_headers():
    expected = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': 'api_key'
    }

    out = util.get_headers('api_key')

    assert expected == out


@pytest.mark.parametrize('route, output', (
    ('users/slugname/history', 'users/slugname/history'),
    ('/users/slugname/history', 'users/slugname/history'),
))
def test_get_endpoint(route, output):
    result = util.get_endpoint(route)

    assert result == (f'https://api.trakt.tv/{output}')


def test_get_history_endpoint():
    expected = 'https://api.trakt.tv/users/testuser/history'

    out = util.get_history_endpoint('testuser')

    assert expected == out


def test_get_trakt_user_with_arg():
    expected = 'arg_user'

    out = util.get_trakt_user('arg_user', 'nick', 'mock_db')

    assert expected == out


def test_get_last_history_item():
    expected = 'lastplay'

    response = unittest.mock.MagicMock()
    response.json.return_value = ['lastplay']

    out = util.get_last_history_item(response)

    assert expected == out


def test_get_last_history_item_no_user():
    response = unittest.mock.MagicMock()
    response.status_code = 404

    with pytest.raises(errors.NoUserException) as e:
        util.get_last_history_item(response)

    assert str(e.value) == 'User does not exist'


def test_get_last_history_item_no_history():
    response = unittest.mock.MagicMock()
    response.json.return_value = []

    with pytest.raises(errors.NoHistoryException) as e:
        util.get_last_history_item(response)

    assert str(e.value) == 'User has no history'
