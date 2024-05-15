from __future__ import annotations


class TraktException(Exception):
    pass


class TraktLinkException(TraktException):
    pass


class NoUserException(TraktException):
    pass


class NoUserSetException(TraktException):
    pass


class NoHistoryException(TraktException):
    pass


class NoPublicHistoryException(NoHistoryException):
    pass
