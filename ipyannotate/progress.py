
from traitlets import Unicode, Instance, List

from .widget import DOMWidget, register_widget
from .colors import COLORS
from .shortcut import KEYS


class Atom(object):
    def __init__(self, color=None, active=False, defined=False):
        self.color = color
        self.active = active
        self.defined = defined

    @property
    def as_json(self):
        return dict(
            color=self.color,
            active=self.active,
            defined=self.defined
        )

    @classmethod
    def from_json(cls, data):
        return cls(**data)


def to_json(atoms, widget):
    return [_.as_json for _ in atoms]


def from_json(data, widget):
    return [Atom.from_json(_) for _ in data]


def generate_atoms(tasks, toolbar):
    for task in tasks:
        color = toolbar.color(task.value)
        active = tasks.is_current(task)
        defined = task.is_defined
        yield Atom(
            color=color,
            active=active,
            defined=defined
        )


@register_widget
class Progress(DOMWidget):
    _view_name = Unicode('ProgressView').tag(sync=True)
    _model_name = Unicode('ProgressModel').tag(sync=True)

    atoms = List(Instance(Atom)).tag(
        sync=True,
        to_json=to_json,
        from_json=from_json
    )

    def __init__(self, atoms=()):
        self.annotation = None
        super(DOMWidget, self).__init__(atoms=atoms)

    @property
    def is_registered(self):
        return self.annotation is not None

    def register(self, annotation):
        if self.is_registered:
            raise RuntimeError('already register: %r' % self)
        self.annotation = annotation

    def update(self):
        toolbar = self.annotation.toolbar
        tasks = self.annotation.tasks
        self.atoms = list(generate_atoms(tasks, toolbar))
