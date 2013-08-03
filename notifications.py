#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib

def pause(player, notification, server, port, www_port):
    paused = notification.endswith('1')
    if paused:
        title = 'Paused'
    else:
        player.fetcher.write('%s current_title ?\n' % player.id)
        title = urllib.unquote(player.fetcher
            .read_until('\n')
            .replace('%s current_title ' % player.id, '')
            .rstrip('\n')
        )
    return title, player.name, None

def new_song(player, notification, server, port, www_port):
    player.fetcher.write('%s status - 1 tags:\n' % player.id)
    track_id = [urllib.unquote(x) for x in player.fetcher.read_until('\n').split(' ') if urllib.unquote(x).startswith('id:')][0].lstrip('id:')
    cache_path = os.path.abspath('./') + '/cache'
    cover_path = '%s/%s.jpg' % (cache_path, track_id,)
    if not os.path.exists(cover_path):
        cover_url = 'http://%s:%i/music/%s/cover.jpg' % (server, www_port, track_id,)
        urllib.urlretrieve(cover_url, cover_path)

    return urllib.unquote(notification.split(' ')[2]), player.name, cover_path
