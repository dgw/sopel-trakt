from __future__ import annotations

import inspect
import sys

import pytest

import sopel_trakt.errors


def get_error_classes():
    def is_class_member(member):
        return (
            inspect.isclass(member)
            and member.__module__ == 'sopel_trakt.errors'
        )

    return [
        member_tuple[1]
        for member_tuple
        in inspect.getmembers(
            sopel_trakt.errors,
            is_class_member,
        )
    ]


@pytest.mark.parametrize(
    'error_class',
    get_error_classes(),
)
def test_error_messages(error_class):
    assert str(error_class('message here')) == 'message here'
