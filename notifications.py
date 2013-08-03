#! /usr/bin/python
# -*- coding: utf-8 -*-

def pause(player, notification):
   body = 'Paused' if notification.endswith('1') else 'Playing'
   return player.name, body, None
