#! /usr/bin/python
# -*- coding: utf-8 -*-

from telnetlib import Telnet
import sys, getopt, re, pynotify, notifications

DEFAULT_ICON_LOCATION = '/home/mmm/kode/squeezebox-notify/resources/squeezebox.jpg'

players = {}
notification = pynotify.Notification('Squuezebox Notification')

class Player():
    name = None

    def __init__(self, name):
        pynotify.init('squeezebox-notify-%s' % name)
        self.name = name

def get_player_info(fetcher, player_mac):
    if not player_mac in players.keys():
        fetcher.write('player name %s ?\n' % player_mac)
        name = fetcher.read_until('\n').replace('player name %s ' % player_mac, '').replace('\n', '')
        players[player_mac] = Player(name)
    return players[player_mac]

def notify(player, cmd):
    # Only show notifications that we know how to handle.
    known_notifications = {
        'playlist pause' : notifications.pause
    }
    for notif in known_notifications.keys():
        if cmd.startswith(notif):
            title, body, icon = known_notifications[notif](player, cmd)
            notification.update(title, body, icon if icon else DEFAULT_ICON_LOCATION)
            notification.show()

def print_help():
    print """
squeezebox-notify

Usage: squeezebox-notify [options] <server>

<server> is IP address or domain name of machine running Logitech Music Server.

Options:

  -p      port number (default is 9090)
"""

if __name__ == '__main__':
    # Get arguments and options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:p:')
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    # Only allow a single argument, the server address.
    if len(args) != 1:
        print_help()
        sys.exit(2)
    else:
        server = args[0]

    # Set server port.
    port = 9090
    for opt, arg in opts:
        if opt == '-p':
            try:
                port = int(arg)
            except ValueError:
                print_help()
    
    # Initialise notifications.
    pynotify.init('squeezebox-notify')
    notification = pynotify.Notification('Squeezebox Notify',
        'Connecting to %s' % (server if port == 9090 else ('%s:%i' % (server, port,))),
        '/home/mmm/kode/squeezebox-notify/resources/squeezebox.jpg')
    notification.show()
    
    # Compile a regex for player related notifications, which are identified by a MAC address and then some.
    player_pattern = re.compile('^(([0-9a-f]{2}%3A){5}[0-9a-f]{2}) (.+)')

    # Start telnet clients (one a as listener, another to fetch info).
    listener = Telnet()
    listener.open(server, port)
    fetcher = Telnet()
    fetcher.open(server, port)
    listener.write('listen 1\n')

    # Start listening for server notifications and process them.
    while True:
        # Get notification data.
        data = listener.read_until('\n')
        # Analyse notification.
        m = player_pattern.match(data)
        # If it looks like a player related notification, break it apart and find out what it's about.
        if m:
            # First, get info about the player.
            player = get_player_info(fetcher, m.group(1))
            # Then, notify.
            notify(player, m.group(3).replace('\n', ''))

