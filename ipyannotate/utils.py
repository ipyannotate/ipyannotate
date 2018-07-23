# coding: utf-8
from __future__ import unicode_literals


def capped_repr(item, cap=80):
    string = repr(item)
    if len(string) > cap:
        string = string[:cap] + '...'
    return string
