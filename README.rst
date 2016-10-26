Roca
=====

Opinionated static documentation generator using Markdown

.. image:: https://img.shields.io/pypi/v/Roca.svg?style=flat-square   :target: https://pypi.python.org/pypi/Roca
.. image:: https://img.shields.io/pypi/l/Roca.svg?style=flat-square   :target: https://pypi.python.org/pypi/Roca
.. image:: https://img.shields.io/pypi/pyversions/Roca.svg?style=flat-square   :target: https://pypi.python.org/pypi/Roca
.. image:: https://img.shields.io/github/issues/Addvilz/roca.svg?style=flat-square   :target: https://github.com/Addvilz/roca/issues

Installation
------------

``pip install roca``

Usage
-----

First, you will need a local install of `Roca Web`_. But don’t worry -
it has no dependencies apart from having a Web browser. Just clone the
repository ``git@github.com:Addvilz/roca-web.git`` somewhere.

Now you can execute Roca command line utility and point it to directory
containing Markdown documents using ``--source`` argument.

Roca will then generate a file called ``data.json``, which you should
then put in the root directory of your `Roca Web`_ installation.

You can optionally pass an argument ``--target`` and provide your
`Roca Web`_ directory as an argument. Roca will then generate data file
in that directory, instead of the current working directory.

Next, just point your browser to index.html of your Roca Web
installation, and that’s it.

::

    roca [-h] --source SOURCE [--target TARGET] [--title TITLE]

      -h, --help       show help message and exit
      --target TARGET  Target directory to generate data.json in
      --title TITLE    Project title

.. _Roca Web: https://github.com/Addvilz/roca-web


Directory structure
--------------------

There aren't many rules for how you should structure your doc's for Roca.
Some things to consider:

1. Directory should contain index.md. This file, if present, will be displayed when you click on directory entry.
2. Files names should be expected titles of the document. Spaces and capitalization is okay.
3. camelCase, snake_case and dash-case file names will be normalized to "Camel case", "Snake case" and "Dash case"

Screenshot
---------------------

Here is a sample output of a GitHub wiki of the `guard/guard`_ project.

.. _guard/guard: https://github.com/guard/guard/wiki

.. image:: http://i.imgur.com/ywMuQ2l.png
