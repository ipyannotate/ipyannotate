# coding: utf-8
from __future__ import unicode_literals

from .tasks import (
    Task as MonoTask,
    MultiTask,
    Tasks
)
from .buttons import (
    OkButton as Ok,
    ErrorButton as Error,
    NextButton as Next,
    BackButton as Back,

)
from .toolbar import (
    Toolbar as MonoToolbar,
    MultiToolbar
)
from .canvas import OutputCanvas
from .annotation import Annotation


def annotate(items, buttons=(), display=None, multi=False):
    if multi:
        Task = MultiTask
        Toolbar = MultiToolbar
    else:
        Task = MonoTask
        Toolbar = MonoToolbar

    tasks = Tasks(Task(_) for _ in items)
    if not buttons:
        buttons = [
            Ok(),
            Error(),
            Back(),
            Next()
        ]
    toolbar = Toolbar(buttons)
    canvas = OutputCanvas(display=display)
    return Annotation(toolbar, tasks, canvas=canvas)
