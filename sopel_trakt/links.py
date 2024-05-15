from __future__ import annotations

import requests

from sopel import plugin

from .errors import TraktLinkException
from .util import get_headers


def minutes_to_hhmm(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f'{hours}h{minutes}m'


@plugin.url(r'https?://trakt.tv/(?P<kind>show|movie)s/(?P<slug>[a-zA-Z0-9-]+)/?')
def link_handler(bot, trigger):
    kind = trigger.group('kind')
    slug = trigger.group('slug')

    if kind == 'show':
        output_show(bot, slug)
    elif kind == 'movie':
        output_movie(bot, slug)
    else:
        raise TraktLinkException("Impossible link encountered")


def output_show(bot, slug):
    url = f'https://api.trakt.tv/shows/{slug}?extended=full'
    headers = get_headers(bot.config.trakt.client_id)

    r = requests.get(url, headers=headers)
    data = r.json()

    parts = []
    parts.append(f"{data['title']} ({data['year']})")
    parts.append(f"{data['runtime']} min/ep")
    parts.append(data['status'].title())
    if data.get('tagline'):
        parts.append(f'"{data['tagline']}"')
    parts.append(data['overview'])

    bot.say(' | '.join(parts), truncation='…')


def output_movie(bot, slug):
    url = f'https://api.trakt.tv/movies/{slug}?extended=full'
    headers = get_headers(bot.config.trakt.client_id)

    r = requests.get(url, headers=headers)
    data = r.json()

    parts = []
    parts.append(f"{data['title']} ({data['year']})")
    parts.append(minutes_to_hhmm(data['runtime']))
    if data.get('tagline'):
        parts.append(data['tagline'])
    parts.append(data['overview'])

    bot.say(' | '.join(parts), truncation='…')
