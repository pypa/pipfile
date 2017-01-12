Pipfile
=======

**Warning**: this project is under active development (and design).

A ``Pipfile`` (named ``Pipfile``, and its sister ``Pipfile.freeze``), is a new (and much better!)
replacement for the existing standard `pip <https://github.com/pypa/pip>`_'s ``requirements.txt``
file. It uses the well-established `TOML <https://github.com/toml-lang/toml>`_ format. 

Specifically, for a Python application, a ``Pipfile`` allows developers to specify
*concrete* and sets of dependencies, their locations, and their loose version
constraints. A ``Pipfile.freeze`` can then be automatically generated during
package installation to fully specify an exact set of known working versions,
and future installations may refer to the ``Pipfile.freeze`` to recreate the
exact contents of the environment in a *deterministic* manner. A deployed web
application, for instance, can be completely redeployed with the same exact
versions of all recursive dependencies, by referencing the ``Pipfile.freeze``
file.

``pip`` will grow a new command line option, ``-p`` / ``--pipfile``  to install
the versions specified in a ``Pipfile``, similar to its existing ``-r`` /
``--requirement`` argument for installing ``requirements.txt`` files.

This repository contains the design specification of the ``Pipfile`` format, as
well as (soon) an implementation of a parser for the specification which can be
used by `pip <https://github.com/pypa/pip>`_ and any other consumer, once the
API (including the form of a ``Pipfile`` itself) has been built out and
finalized.

The Concept
-----------

A Pipfile (``Pipfile``) will be superior to a ``requirements.txt`` file in a number of
ways:

* TOML syntax for declaring all types of Python dependencies.
* One Pipfile (as opposed to multiple ``requirements.txt`` files).

  * Existing requirements files tend to proliferate into e.g.
    ``dev-requirements.txt``, ``test-requirements.txt``, etc., but a
    ``Pipfile`` will allow seamlessly specifying groups of dependencies
    in one place.
  * This will be surfaced as only two built-in groups (*default* &
    *development*).
  * Custom groups may be added in the future. Remember, it is easier
    to add features in the future than it is to remove them. The Composer
    community has been successful with only *default* and *development*
    as group options for many years — I'd like to follow this model, at
    first.

* Fully specified (and *deterministic*) environments in the form of
  ``Pipfile.freeze``.


Example Pipfile
+++++++++++++++

Note—this is an evolving work in progress; filename is ``Pipfile``::

    [[source]]
    url = 'https://pypi.org/'
    verify_ssl = true

    [requires]
    python_version = '2.7'

    [packages]
    requests = { extras = ['socks'] }
    Django = '>1.10'
    pinax = { git = 'git://github.com/pinax/pinax.git', ref = '1.4', editable = true }

    [dev-packages]
    nose = '*'

Notes:

- There will be a default source.
- Requires utilizes  `PEP 508 <https://www.python.org/dev/peps/pep-0508/#environment-markers>`_
  ``marker =  'specifier'`` markers. This functionality may not be readily used, as it 
  is only to assert (and therefore abort, if appropriate) installation on certain platforms 
  (e.g. windows, wrong python version).

PEP 508 Support (aborts if not True)::

    # Support for all PEP 508 markers
    [requires]
    python_full_version = '3.6.0b1'

    platform = 'windows'


Example Pipfile.freeze
++++++++++++++++++++++

Note—this file is always to be generated, not modified or constructed by a
user::

  {
      "_meta": {
          "Pipfile-sha256": "73d81f4fbe42d1da158c5d4435d921121a4a1013b2f0dfed95367f3c742b88c6",
          "requires": [
              {"marker": "python_version", "specifier": "2.7"}
          ],
          "sources": [
              {"url": "https://pypi.org/", "verify_ssl": true},
          ]
       },
      "default": [
          {"name": "Django", "version": "1.10.3", "hash": "..."},
          {"name": "requests", "version": "2.12.1", "hash": "..."},
          {"name": "pinax", "git": "git://...", "ref": "1.4", "editable": true},
          {"name": "PySocks", "version": "1.5.6", "hash": "..."},
      ],
      "development": [
          {"name": "nose", "version": "1.3.7", "hash": "..."},
      ]
  }


Note how the versions of each dependency are recursively frozen, and a hash
gets computed so that you can take advantage of
`new pip security features
<https://pip.pypa.io/en/stable/reference/pip_install/#hash-checking-mode>`_

Why not TOML & Friends?
///////////////////////

TOML is an attractive option for ``Pipfile``, especially with the recent
`PEP 518 (pyproject.tml) <https://www.python.org/dev/peps/pep-0518/>`_ plans that are in place.

Don't worry — this and other formats are possibly being considered for
the contents ``Pipfile``.

The focus at the moment is on getting the Python representation perfect before
proceeding with true `prototypes <https://gist.github.com/kennethreitz/9319936c301be5c01f6da04e518d2cf3>`_
with existing markup languages.  However, we are optimizing for *ease of typing* for the end-user (**no
googling / boilerplate / copypasta required!**), so the Python-esque syntax
(AST-powered) will, at this time, likely exist in the final version. But,
this is being constantly re-evaluated.

It's all about making an API for Humans, first. Machines, second. Ideally,
both of these can co-exist in harmony. For example, if this Python-esque syntax
is settled on, a parser (this library, actually) will be readily available and
may have a command-line utility for converting the representation to JSON.


Example Pip Integration (eventually)
++++++++++++++++++++++++++++++++++++

Install packages from ``Pipfile``::

    $ pip install -p
    ! Warning: Pipfile.freeze (48d35f) is out of date. Updating to (73d81f).
    Installing packages from requirements.piplock...

    # Manually update lockfile.
    $ pip freeze -p special_pipfile
    special_pipfile.freeze (73d81f) written to disk.

Notes::

    # -p accepts a path argument, which defaults to 'Pipfile'.
    # Pipfile.freeze will be written automatically during `install -p` if it does not exist.

Ideas::

- Recursively look for `Pipfile` in parent directories (limit 3/4?) when ``-p`` is bare.


Useful Links
------------

- `pypa/pip#1795: Requirements 2.0 <https://github.com/pypa/pip/issues/1795>`_
- `Basic Concept Gist <https://gist.github.com/kennethreitz/4745d35e57108f5b766b8f6ff396de85>`_ (fork of @dstufft's)

Inspirations
++++++++++++

- `nvie/pip-tools: A set of tools to keep your pinned Python dependencies fresh. <https://github.com/nvie/pip-tools>`_
- `A Better Pip Workflow by Kenneth Reitz <https://www.kennethreitz.org/essays/a-better-pip-workflow>`_
- Taking lessons-learned from Composer, Cargo, Yarn, NPM, Bundler, and friends.

Documentation
-------------

The `documentation`_ for this project will (eventually) reside at pypi.org.


Discussion
----------

If you run into bugs, you can file them in our `issue tracker`_.

You can also join ``#pypa`` on Freenode to ask questions or get involved.


.. _`documentation`: https://pipfile.pypa.io/
.. _`issue tracker`: https://github.com/pypa/pipfile/issues


Code of Conduct
---------------

Everyone interacting in the pipfile project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
