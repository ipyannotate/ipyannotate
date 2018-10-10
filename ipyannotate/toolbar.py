# coding: utf-8
from __future__ import unicode_literals

from collections import Counter

from traitlets import (
    Unicode, Instance, List,
    observe, validate
)

from .widget import DOMWidget, register_widget, widget_serialization
from .buttons import Button, has_value, is_control


def assert_uniq(items):
    cache = set()
    for item in items:
        if item in cache:
            raise ValueError('expected unique, duplicate: %r' % item)
        cache.add(item)
    return True


def diff_buttons(a, b):
    mapping = {id(_): _ for _ in a + b}
    a = {id(_) for _ in a}
    b = {id(_) for _ in b}
    removed = [mapping[_] for _ in a - b]
    added = [mapping[_] for _ in b - a]
    return removed, added


class Stats(Counter):
    def add(self, button):
        self[id(button)] += 1

    def remove(self, button):
        self[id(button)] -= 1

    def assert_free(self, button):
        if self[id(button)] > 0:
            raise RuntimeError('button in use: %r' % button)


@register_widget
class Toolbar(DOMWidget):
    _view_name = Unicode('ToolbarView').tag(sync=True)
    _model_name = Unicode('ToolbarModel').tag(sync=True)

    buttons = List(Instance(Button)).tag(sync=True, **widget_serialization)

    def __init__(self, buttons):
        self.stats = Stats()
        self.annotation = None
        super(Toolbar, self).__init__(buttons=buttons)
        self.observe(self.update_buttons, 'buttons', type='change')

    @property
    def is_registered(self):
        return self.annotation is not None

    def register(self, annotation):
        if self.is_registered:
            raise RuntimeError('already register: %r' % self)
        self.annotation = annotation
        for button in self.buttons:
            button.register(annotation)

    @validate('buttons')
    def validate_buttons(self, data):
        buttons = data['value']
        assert_uniq(_.value for _ in buttons if has_value(_))
        assert_uniq(_.shortcut for _ in buttons if _.shortcut)
        removed, added = diff_buttons(self.buttons, buttons)
        for button in removed:
            self.stats.assert_free(button)
        return buttons

    def update_buttons(self, data):
        removed, added = diff_buttons(data['old'], data['new'])
        for button in added:
            button.register(self.annotation)

    def find(self, shortcut):
        for button in self.buttons:
            if button.shortcut == shortcut:
                return button

    def handle_click(self, button):
        task = self.annotation.tasks.current
        if button.active:
            task.unset()
            self.stats.remove(button)
        else:
            task.set(button.value)
            self.stats.add(button)
        self.annotation.next()

    def update(self, value):
        for button in self.buttons:
            if has_value(button):
                active = button.value == value
                button.active = active

    def color(self, value):
        for button in self.buttons:
            if has_value(button) and button.value == value:
                return button.color


def assert_controls(buttons):
    for button in buttons:
        if is_control(button):
            return
    raise ValueError('extected control buttons')


class MultiToolbar(Toolbar):
    def __init__(self, buttons):
        assert_controls(buttons)
        super(MultiToolbar, self).__init__(buttons)

    def handle_click(self, button):
        task = self.annotation.tasks.current
        value = button.value
        if button.active:
            task.remove(value)
            self.stats.remove(button)
        else:
            task.add(value)
            self.stats.add(button)
        self.annotation.update()

    def update(self, value):
        for button in self.buttons:
            if has_value(button):
                active = button.value in value
                button.active = active

    def color(self, value):
        for button in self.buttons:
            if has_value(button) and button.value in value:
                return button.color
