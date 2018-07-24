# coding: utf-8
from __future__ import unicode_literals

from traitlets import Unicode, Bool, Enum, Any

from .utils import shorten
from .shortcut import KEYS
from .widget import DOMWidget, register_widget
from .colors import COLORS, GRAY, BLUE, RED, GREEN


@register_widget
class Button(DOMWidget):
    _view_name = Unicode('ButtonView').tag(sync=True)
    _model_name = Unicode('ButtonModel').tag(sync=True)

    color = Enum(COLORS).tag(sync=True)
    icon = Unicode(allow_none=True).tag(sync=True)
    label = Unicode(allow_none=True).tag(sync=True)
    shortcut = Enum(KEYS, allow_none=True).tag(sync=True)
    active = Bool(False).tag(sync=True)

    def __init__(self, color=GRAY, icon=None, label=None, shortcut=None):
        super(Button, self).__init__(
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )
        self.annotation = None
        self.on_msg(self.handle_message)

    @property
    def is_registered(self):
        return self.annotation is not None

    def register(self, annotation):
        if self.is_registered:
            raise RuntimeError('already register: %r' % self)
        self.annotation = annotation

    def assert_registered(self):
        if not self.is_registered:
            raise RuntimeError('not registered')

    def handle_click(self):
        raise NotImplemented

    def handle_message(self, _, content, buffers):
        event = content['event']
        if event == 'click':
            self.handle_click()

    def click(self):
        self.send({'event': 'click'})


class ValueButton(Button):
    value = Any()

    def __init__(self, value, color=GRAY, icon=None, label=None, shortcut=None):
        if label is None:
            label = shorten(str(value), cap=10)
        super(ValueButton, self).__init__(
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )
        self.value = value

    def handle_click(self):
        self.assert_registered()
        self.annotation.toolbar.handle_click(self)


def has_value(item):
    return isinstance(item, ValueButton)


class OkButton(ValueButton):
    def __init__(self, value=True, color=GREEN, icon='👌', label='ok', shortcut='1'):
        super(OkButton, self).__init__(
            value=value,
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )


class ErrorButton(ValueButton):
    def __init__(self, value=False, color=RED, icon='❌', label='err', shortcut='2'):
        super(ErrorButton, self).__init__(
            value=value,
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )


class ControlButton(Button):
    pass


def is_control(item):
    return isinstance(item, ControlButton)


class NextButton(ControlButton):
    def __init__(self, color=GRAY, icon='→ ', label='next', shortcut='j'):
        super(NextButton, self).__init__(
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )

    def handle_click(self):
        self.assert_registered()
        self.annotation.next()


class BackButton(ControlButton):
    def __init__(self, color=GRAY, icon='← ', label='back', shortcut='k'):
        super(BackButton, self).__init__(
            color=color,
            icon=icon,
            label=label,
            shortcut=shortcut
        )

    def handle_click(self):
        self.assert_registered()
        self.annotation.back()
