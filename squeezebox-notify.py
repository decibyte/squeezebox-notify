#! /usr/bin/python
# -*- coding: utf-8 -*-

from telnetlib import Telnet
import pynotify

pynotify.init('squeezebox-notify')
n = pynotify.Notification('Squeezebox Notify', 'Connected to *****', '/home/mmm/kode/squeezebox-notify/resources/squeezebox.jpg')
n.show()
