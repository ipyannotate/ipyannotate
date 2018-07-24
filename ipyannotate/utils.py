# coding: utf-8
from __future__ import unicode_literals


def shorten(string, cap=80):
    if len(string) > cap:
        string = string[:cap] + '...'
    return string
