from __future__ import annotations

from datetime import datetime, timezone

import requests

from sopel import plugin
from sopel.formatting import bold, hex_color, italic
from sopel.tools.time import seconds_to_human

from .errors import TraktLinkException
from .util import BRAND_COLORS, get_headers, parse_timestamp


def minutes_to_hhmm(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f'{hours}h{minutes}m'


@plugin.url(
    r'https?://trakt.tv/(?P<kind>show|movie|user)s/(?P<slug>[a-zA-Z0-9-]+)/?')
def link_handler(bot, trigger):
    kind = trigger.group('kind')
    slug = trigger.group('slug')

    if kind == 'show':
        output_show(bot, slug)
    elif kind == 'movie':
        output_movie(bot, slug)
    elif kind == 'user':
        output_user(bot, slug)
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


def output_user(bot, slug):
    url = f'https://api.trakt.tv/users/{slug}?extended=full,vip'
    headers = get_headers(bot.config.trakt.client_id)

    r = requests.get(url, headers=headers)
    data = r.json()

    parts = []

    basic_info = ''
    if data.get('private'):
        basic_info += italic('Private profile') + ' '
    else:
        basic_info += bold(data['name']) + ' '
    basic_info += f'(@{data['username']}) '
    if data.get('vip'):
        basic_info += hex_color(
            '\u202fVIP\u202f', BRAND_COLORS.VIP_TEXT, BRAND_COLORS.VIP)
        if data.get('vip_ep'):
            basic_info += hex_color(
                '\u202fEP\u202f', BRAND_COLORS.VIP_TEXT, BRAND_COLORS.VIP_EP)
        elif data.get('vip_og'):
            basic_info += hex_color(
                '\u202fOG\u202f', BRAND_COLORS.VIP_TEXT, BRAND_COLORS.VIP_OG)
        if vip_years := data.get('vip_years'):
            # don't output this for 0 years; it'd look weird
            basic_info += f' {vip_years}\U0001F7CA'
    parts.append(basic_info)

    if age := data.get('age'):
        parts.append(f'{age} years old')

    if join_time := data.get('joined_at'):
        join_time = parse_timestamp(join_time)
        since = seconds_to_human(
            datetime.now(tz=timezone.utc) - join_time
        )
        parts.append(f'Member since {join_time.year} ({since})')

    if location := data.get('location'):
        parts.append(f'📍 {location}')

    if about := data.get('about'):
        parts.append(about)

    bot.say(' | '.join(parts), truncation='…')
