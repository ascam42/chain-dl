#!/usr/bin/env python3

"""
    User configuration parsing
"""

import          log
from chaindl    import *


CONFIG_ERR  =   -2



def get_specs(dl_config):
    """
        Function that retrives all useful user's config data.
        Raises errors on missing/invalid contents.
    """
    ret = {}

    if not DOWNLOAD in dl_config:
        log.ko("No '" + DOWNLOAD + "' scope found in config")
        __die_invalid_config()
    if not URL in dl_config[DOWNLOAD] or \
       not LIST_CONTAINER_CLASS in dl_config[DOWNLOAD] or \
       not CONTENT_CONTAINER_CLASS in dl_config[DOWNLOAD]:
        log.ko("Missing one or more required fields in scope '"
                + DOWNLOAD + "'")
        log.ko("Fields:",
                URL, LIST_CONTAINER_CLASS, CONTENT_CONTAINER_CLASS,
                "are mandatory")
        __die_invalid_config()

    ret[URL] = dl_config[DOWNLOAD][URL]
    ret[PREFERRED_HOST] = __get_best_host(dl_config)
    ret[IGNORE_HOSTS] = __get_ignored_hosts(dl_config)
    ret[TIMEOUT] = __get_timeout(dl_config)
    ret[TITLE] = __get_show_title(dl_config)
    ret[CONTENT_CONTAINER_CLASS] = dl_config[DOWNLOAD][CONTENT_CONTAINER_CLASS]
    ret[LIST_CONTAINER_CLASS] = dl_config[DOWNLOAD][LIST_CONTAINER_CLASS]
    if CONTENT_CONTAINER_ID in dl_config[DOWNLOAD]:
        ret[CONTENT_CONTAINER_ID] = dl_config[DOWNLOAD][CONTENT_CONTAINER_ID]
    if LIST_CONTAINER_ID in dl_config[DOWNLOAD]:
        ret[LIST_CONTAINER_ID] = dl_config[DOWNLOAD][LIST_CONTAINER_ID]
    ret[START_EPISODE] = __get_start_episode(dl_config)
    ret[IGNORE_EPISODES] = __get_ignore_episodes(dl_config)
    return (ret)


def __die_invalid_config():
    log.ko("Invalid (or inexistant) download configuration file")
    log.ko("Please make sure you have a valid and readable configuration file")
    exit(CONFIG_ERR)


def __get_show_title(dl_config):
    """
        Return user's config show title
    """
    show_title = None

    if ANIME in dl_config:
        if TITLE in dl_config[ANIME]:
            show_title = dl_config[ANIME][TITLE]
    return (show_title)


def __get_best_host(dl_config):
    """
        Return user's config best video host
    """
    best_host = None

    if PREFERRED_HOST in dl_config[DOWNLOAD]:
        best_host = dl_config[DOWNLOAD][PREFERRED_HOST]
        if not best_host.startswith("http://"):
            best_host = "http://" + best_host
    return (best_host)


def __get_ignored_hosts(dl_config):
    """
        Return user's config video hosts to be ignored
    """
    ignore_hosts = []

    if IGNORE_HOSTS in dl_config[DOWNLOAD]:
        for host in dl_config[DOWNLOAD][IGNORE_HOSTS].split(' '):
            ignore_hosts.append(host)
    return (ignore_hosts)


def __get_timeout(dl_config):
    """
        Return user's config HTTP requests timeout
    """
    timeout = DEFAULT_TIMEOUT

    if TIMEOUT in dl_config[DOWNLOAD]:
        try:
            timeout = int(dl_config[DOWNLOAD][TIMEOUT])
        except ValueError:
            timeout = DEFAULT_TIMEOUT
    return (timeout)


def __get_start_episode(dl_config):
    """
        Return user's config episode number
        at which download shall be started
    """
    start_episode = 0

    if START_EPISODE in dl_config[DOWNLOAD]:
        try:
            start_episode = int(dl_config[DOWNLOAD][START_EPISODE])
        except ValueError:
            start_episode = 0
    return (start_episode)


def __get_ignore_episodes(dl_config):
    """
        Return user's config episodes number
        that shall be ignored
    """
    ignore_episodes = []

    if IGNORE_EPISODES in dl_config[DOWNLOAD]:
        for episode in dl_config[DOWNLOAD][IGNORE_EPISODES].split(' '):
            try:
                ignore_episodes.append(int(episode))
            except ValueError:
                pass
    return (ignore_episodes)

