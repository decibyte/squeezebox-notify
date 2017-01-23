#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib

# TODO: Move this one to the player class
def get_cover_path(server, www_port, track_id, username=None, password=None):
    # TODO: Rewrite to support HTTPS and authentication. The code below doesn't
    # work at all.
    return None

    cache_path = '/'.join(os.path.abspath(__file__).split('/')[:-1]) + '/cache'
    cover_path = '%s/%s.jpg' % (cache_path, track_id,)
    if not os.path.exists(cover_path):
        cover_url = 'https://%s:%s@%s:%i/music/%s/cover.jpg' % (
            username,
            password,
            server,
            www_port,
            track_id,
        )
        urllib.urlretrieve(cover_url, cover_path)

    return cover_path

def pause(player, notification, server, port, www_port, username=None, password=None):
    paused = notification.endswith('1')
    if paused:
        title = 'Paused'
    else:
        title = player.get_current_title()
    return title, player.name, None if paused else get_cover_path(server, www_port, player.get_track_id())

def new_song(player, notification, server, port, www_port, username=None, password=None):
    return urllib.unquote(notification.split(' ')[2]), player.name, get_cover_path(server, www_port, player.get_track_id())
