Rocadocs
========

Opinionated static documentation generator using Markdown

.. image:: https://img.shields.io/pypi/v/rocadocs.svg?style=flat-square   :target: https://pypi.python.org/pypi/rocadocs
.. image:: https://img.shields.io/pypi/l/rocadocs.svg?style=flat-square   :target: https://pypi.python.org/pypi/rocadocs
.. image:: https://img.shields.io/pypi/pyversions/rocadocs.svg?style=flat-square   :target: https://pypi.python.org/pypi/rocadocs
.. image:: https://img.shields.io/github/issues/rocadocs/rocadocs.svg?style=flat-square   :target: https://github.com/rocadocs/rocadocs/issues

Installation
------------

``pip install rocadocs``

Features
--------

1. Github flavoured Markdown support, including task lists
2. ``[TOC]`` support
3. Fenced and inline code blocks
4. rST style `admonitions`_
5. Aesthetic values are of great importance

.. _admonitions: http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions

How it works
------------

Rocadocs is a two part system. It consists of a command line tool written in Python - it converts a directory tree
of Markdown documents to a JSON datafile. This file can then be served by `rocadocs/web`_, a client-side application
written in Vue.js.

Usage
-----

First, you will need a `rocadocs/web`_ set up somewhere. `rocadocs/web`_ contains all the static files and frontend data required
to serve the generated documentation. You can fetch the sources automatically using ``rocadocs-web --dir DIR`` command where
DIR is the directory where you want to install the static assets.

Alternatively, you can install static assets using these commands:

::

    wget https://raw.githubusercontent.com/rocadocsgit/web/master/dist/rocaweb.tar.gz
    tar -xvf rocaweb.tar.gz


Now you can execute Roca command line utility and point it to directory
containing Markdown documents using ``--source`` argument.

Roca will then generate a file called ``data.json``, which you should
then put in the root directory of your `rocadocs/web`_ installation.

You can optionally pass an argument ``--target`` and provide your
`rocadocs/web`_ directory as an argument. Roca will then generate data file
in that directory, instead of the current working directory.

Next, just point your browser to index.html of your rocadocs/web
installation, and that’s it.

::

    rocadocs [-h] --source SOURCE [--target TARGET] [--title TITLE]

      -h, --help       show help message and exit
      --target TARGET  Target directory to generate data.json in
      --title TITLE    Project title

.. _rocadocs/web: https://github.com/Addvilz/roca-web


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