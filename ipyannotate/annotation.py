# coding: utf-8
from __future__ import unicode_literals

from traitlets import Instance, Unicode, observe
from .widget import DOMWidget, register_widget, widget_serialization

from .shortcut import decode_key
from .toolbar import Toolbar
from .progress import Progress
from .canvas import Canvas, OutputCanvas
from .tasks import Tasks


@register_widget
class Annotation(DOMWidget):
    _view_name = Unicode('AnnotationView').tag(sync=True)
    _model_name = Unicode('AnnotationModel').tag(sync=True)

    toolbar = Instance(Toolbar).tag(sync=True, **widget_serialization)
    progress = Instance(Progress).tag(sync=True, **widget_serialization)
    canvas = Instance(Canvas).tag(sync=True, **widget_serialization)
    tasks = Instance(Tasks)

    def __init__(self, toolbar, tasks, progress=None, canvas=None):
        if canvas is None:
            canvas = OutputCanvas()
        if progress is None:
            progress = Progress()
        super(Annotation, self).__init__(
            toolbar=toolbar,
            progress=progress,
            canvas=canvas,
            tasks=tasks
        )
        self.toolbar.register(self)
        self.progress.register(self)
        self.on_msg(self.handle_message)
        self.observe(self.update_toolbar, 'toolbar', type='change')
        self.observe(self.update_progress, 'progress', type='change')
        self.observe(self.update_canvas, 'canvas', type='change')
        self.observe(self.update_tasks, 'tasks', type='change')
        self.update()

    def update_toolbar(self, data):
        toolbar = data['new']
        toolbar.register(self)
        self.update()

    def update_progress(self, data):
        progress = data['new']
        progress.register(self)
        self.update()

    def update_canvas(self, data):
        self.update()

    def update_tasks(self, data):
        self.update()

    def handle_keypress(self, key):
        button = self.toolbar.find(shortcut=key)
        if button:
            button.click()

    def handle_message(self, _, content, buffers):
        event = content['event']
        if event == 'keypress':
            code = content['code']
            key = decode_key(code)
            if key:
                self.handle_keypress(key)

    def update(self):
        task = self.tasks.current
        self.toolbar.update(task.value)
        self.progress.update()
        self.canvas.render(task.output)

    def next(self):
        self.tasks.next()
        self.update()

    def back(self):
        self.tasks.back()
        self.update()
