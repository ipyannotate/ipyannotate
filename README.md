ipyannotate
===========

Jupyter Widget for data annotation

Installation
------------

To install use pip:

    $ pip install ipyannotate
    $ jupyter nbextension enable --py --sys-prefix ipyannotate


For a development installation (requires npm),

    $ git clone https://github.com/alexanderkuk/ipyannotate.git
    $ cd ipyannotate
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipyannotate
    $ jupyter nbextension enable --py --sys-prefix ipyannotate
