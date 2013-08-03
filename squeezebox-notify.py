#! /usr/bin/python
# -*- coding: utf-8 -*-

from telnetlib import Telnet
import sys, getopt, pynotify


def print_help():
    print """
squeezebox-notify

Usage: squeezebox-notify [options] <server>

<server> is IP address or domain name of machine running Logitech Music Server.

Options:

  -p      port number (default is 9090)
"""

if __name__ == '__main__':
    # Get arguments and options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:p:')
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    # Only allow a single argument, the server address
    if len(args) != 1:
        print_help()
        sys.exit(2)
    else:
        server = args[0]

    # Set server port
    port = 9090
    for opt, arg in opts:
        if opt == '-p':
            try:
                port = int(arg)
            except ValueError:
                print_help()

    pynotify.init('squeezebox-notify')
    n = pynotify.Notification('Squeezebox Notify', 'Connecting to %s' % (server if port == 9090 else ('%s:%i' % (server, port,))), '/home/mmm/kode/squeezebox-notify/resources/squeezebox.jpg')
    n.show()
