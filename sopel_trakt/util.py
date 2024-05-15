from __future__ import annotations


def get_headers(client_id):
    return {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }
