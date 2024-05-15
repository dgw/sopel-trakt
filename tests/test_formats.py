from __future__ import annotations

from pathlib import Path

import json
import unittest.mock

from sopel_trakt import formats


def open_json_sample(name):
    path = Path(__file__).parent / ('sample-' + name + '.json')
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def test_episode():
    expected = 'show 1x01 - title'

    out = formats.episode('show', '1', '1', 'title')

    assert expected == out


def test_movie():
    expected = 'film (year)'

    out = formats.movie('film', 'year')

    assert expected == out


def test_last_watched_episode():
    data = open_json_sample('history-episode')[0]

    expected = 'dgw last watched: Wings 5x14 - The Faygitive'

    out = formats.last_watched('dgw', data)

    assert expected == out


def test_last_watched_movie():
    data = open_json_sample('history-movie')[0]

    expected = 'dgw last watched: Liz and the Blue Bird (2018)'

    out = formats.last_watched('dgw', data)

    assert expected == out


@unittest.mock.patch('sopel_trakt.formats.episode')
@unittest.mock.patch('sopel_trakt.formats.movie')
def test_format_output_episode(mock_movie_format, mock_ep_format):
    json = {
        'type': 'episode',
        'show': {'title': 'title'},
        'episode': {
            'season': 'season',
            'number': 'episode',
            'title': 'title'
        }
    }

    formats.last_watched('testuser', json)

    mock_ep_format.assert_called_once()
    assert not mock_movie_format.called


@unittest.mock.patch('sopel_trakt.formats.episode')
@unittest.mock.patch('sopel_trakt.formats.movie')
def test_format_output_movie(mock_movie_format, mock_ep_format):
    json = {
        'type': 'movie',
        'movie': {
            'title': 'title',
            'year': 'year'
        }
    }

    formats.last_watched('testuser', json)

    mock_movie_format.assert_called_once()
    assert not mock_ep_format.called
