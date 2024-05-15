from __future__ import annotations

from . import errors


def last_watched(user, json):
    if json['type'] == 'episode':
        content = episode(
            json['show']['title'],
            json['episode']['season'],
            json['episode']['number'],
            json['episode']['title'],
        )
    elif json['type'] == 'movie':
        content = movie(
            json['movie']['title'],
            json['movie']['year'],
        )
    else:
        raise errors.TraktException('Unknown history item type')

    return f'{user} last watched: {content}'


def episode(show, season, episode, title):
    pad_episode = str(episode).zfill(2)
    return f'{show} {season}x{pad_episode} - {title}'


def movie(title, year):
    return f'{title} ({year})'
