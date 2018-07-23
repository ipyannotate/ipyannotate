# coding: utf-8
from __future__ import unicode_literals

from ipywidgets import (
    DOMWidget,
    widget_serialization,
    register as register_widget
)
from traitlets import Unicode


class DOMWidget(DOMWidget):
    _view_module = Unicode('ipyannotate').tag(sync=True)
    _model_module = Unicode('ipyannotate').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
