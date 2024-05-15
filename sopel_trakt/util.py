from __future__ import annotations

from . import errors


def get_headers(client_id):
    return {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }


def get_endpoint(route):
    if route[0] == '/':
        route = route[1:]

    return f'https://api.trakt.tv/{route}'


def get_history_endpoint(user):
    return get_endpoint(f'users/{user}/history')


def get_trakt_user(arg, nick, db):
    if arg:
        return arg

    trakt_user = db.get_nick_value(nick, 'trakt_user')
    if trakt_user:
        return trakt_user

    raise errors.NoUserSetException


def get_last_history_item(response):
    if response.status_code == 404:
        raise errors.NoUserException('User does not exist')

    if response.status_code == 401:
        raise errors.NoPublicHistoryException("User's profile is private")

    if len(response.json()) == 0:
        raise errors.NoHistoryException('User has no history')

    return response.json()[0]
