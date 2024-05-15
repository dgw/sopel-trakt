from __future__ import annotations

import requests

from sopel import plugin
from sopel.config import types

from . import formats, util
from .errors import (
    NoUserException,
    NoUserSetException,
    NoHistoryException,
)
from .links import link_handler  # noqa


class TraktSection(types.StaticSection):
    client_id = types.SecretAttribute('client_id', default=types.NO_DEFAULT)


def setup(bot):
    bot.config.define_section('trakt', TraktSection)


def configure(config):
    config.define_section('trakt', TraktSection, validate=False)
    config.trakt.configure_setting('client_id', 'Enter Trakt client ID:')


@plugin.commands('trakt')
def trakt_command(bot, trigger):
    client_id = bot.config.trakt.client_id

    try:
        user = util.get_trakt_user(trigger.group(3), trigger.nick, bot.db)
    except NoUserSetException:
        bot.reply(
            "User not set; use {}traktset or pass user as argument"
            .format(bot.config.core.help_prefix)
        )
        return

    api_url = util.get_history_endpoint(user)
    headers = util.get_headers(client_id)
    r = requests.get(api_url, headers=headers)

    try:
        last_play = util.get_last_history_item(r)
    except (NoUserException, NoHistoryException) as e:
        bot.say(str(e))
        return

    out = formats.last_watched(user, last_play)
    bot.say(out)


@plugin.commands('traktset')
def traktset(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('no user given')
        return

    bot.db.set_nick_value(trigger.nick, 'trakt_user', user)

    bot.say(f'{trigger.nick}\'s trakt user is now set as {user}')
