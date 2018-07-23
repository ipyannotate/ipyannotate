from ._version import version_info, __version__

from .api import annotate


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'ipyannotate',
        'require': 'ipyannotate/extension'
    }]
