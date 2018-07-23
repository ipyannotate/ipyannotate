# coding: utf-8
from __future__ import unicode_literals


KEY_CODES = {
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    '0': 48,
    '-': 45,
    '=': 61,
    'q': 113,
    'w': 119,
    'e': 101,
    'r': 114,
    't': 116,
    'y': 121,
    'u': 117,
    'i': 105,
    'o': 111,
    'p': 112,
    '[': 91,
    ']': 93,
    'a': 97,
    's': 115,
    'd': 100,
    'f': 102,
    'g': 103,
    'h': 104,
    'j': 106,
    'k': 107,
    'l': 108,
    ';': 59,
    "'": 39,
    '\\': 92,
    'z': 122,
    'x': 120,
    'c': 99,
    'v': 118,
    'b': 98,
    'n': 110,
    'm': 109,
    ',': 44,
    '.': 46,
    '/': 47,
}
CODE_KEYS = {
    code: key
    for key, code in KEY_CODES.items()
}
KEYS = sorted(KEY_CODES)


def decode_key(code):
    return CODE_KEYS.get(code)
