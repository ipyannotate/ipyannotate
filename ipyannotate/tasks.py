# coding: utf-8
from __future__ import unicode_literals

from .utils import shorten


class Task(object):
    def __init__(self, output, value=None):
        self.output = output
        self.value = value

    @property
    def is_defined(self):
        return self.value is not None

    def set(self, value):
        self.value = value

    def unset(self):
        self.value = None

    @property
    def as_multi(self):
        value = self.value
        if value is not None:
            value = {value}
        return MultiTask(self.output, value)

    def __repr__(self):
        return '{name}(output={output}, value={value})'.format(
            name=self.__class__.__name__,
            output=shorten(repr(self.output)),
            value=self.value
        )


class MultiTask(Task):
    def __init__(self, output, value=None):
        super(MultiTask, self).__init__(output)
        if value is None:
            value = set()
        if not isinstance(value, set):
            raise ValueError('expected set, got %r' % value)
        self.value = value

    @property
    def is_defined(self):
        return bool(self.value)

    def add(self, value):
        self.value.add(value)

    def remove(self, value):
        self.value.remove(value)


class Tasks(list):
    def __init__(self, items):
        self.index = -1
        self.current = None
        for item in items:
            self.append(item)
        if not self:
            raise ValueError('empty tasks')
        self.next()

    def is_current(self, task):
        return id(task) == id(self.current)

    def append(self, task):
        if not isinstance(task, Task):
            raise ValueError('expected Task, got %r' % task)
        list.append(self, task)

    def next(self):
        if not self:
            return
        if self.index < len(self) - 1:
            self.index += 1
        self.current = self[self.index]

    def back(self):
        if not self:
            return
        if self.index > 0:
            self.index -= 1
        self.current = self[self.index]
