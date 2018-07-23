# coding: utf-8
from __future__ import unicode_literals

from IPython import display as ipython
from ipywidgets import Output


class Canvas(object):
    def render(self, item):
        raise NotImplemented


class OutputCanvas(Output, Canvas):
    def __init__(self, display=None):
        Output.__init__(self)
        if not display:
            display = ipython.display
        self.display = display

    def render(self, item):
        with self:
            ipython.clear_output(wait=True)
            self.display(item)
