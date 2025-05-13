from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from . import errors


class BRAND_COLORS(StrEnum):
    """Trakt brand colors, in RGB hex."""
    VIP = 'ED1C24'
    VIP_EP = 'B50D13'
    VIP_OG = VIP_EP
    VIP_TEXT = 'FFF'


def parse_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)


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
