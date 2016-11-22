Pipfile
=======

**Warning**: this project is under active development.

A ``Pipfile``, and its related ``Pipfile.lock``, are a new (and much better!)
replacement for `pip <https://github.com/pypa/pip>`_'s ``requirements.txt``
files.

Specifically, for a Python package, a ``Pipfile`` allows developers to specify
*concrete* sets of its dependencies, their locations, and their loose version
constraints. A ``Pipfile.lock`` can then be automatically generated during
package installation to fully specify an exact set of known working versions,
and future installations may refer to the ``Pipfile.lock`` to recreate the
exact contents of the environment. A deployed web application, for instance,
can be completely redeployed with the same exact versions of all recursive
dependencies, by referencing the ``Pipfile.lock`` file.

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

A ``Pipfile`` will be superior to a ``requirements.txt`` file in a number of
ways:

* Expressive syntax for declaring all types of Python dependencies
* One file, not many
  * Existing requirements files tend to proliferate into e.g.
    ``dev-requirements.txt``, ``test-requirements.txt``, etc., but a
    ``Pipfile`` will allow seamlessly specifying groups of dependencies
    in one place
* Fully specified environments in the form of ``Pipfile.lock``


Example Pipfile
+++++++++++++++

Note—this is an evolving work in progress::

  # Note: There will be a default source, and context manager can also be used.
  source('https://pypi.org/', verify_ssl=True)

  package('requests')
  package('Django', '==1.6')
  package('pinax', git='git://github.com/pinax/pinax.git', ref='1.4', editable=True)
  dev_package('nose')

Example Pipfile.lock
++++++++++++++++++++

Note—this file is always to be generated, not modified or constructed by a
user::

  {
      "_meta": {
          "Pipfile-sha256": "73d81f4fbe42d1da158c5d4435d921121a4a1013b2f0dfed95367f3c742b88c6",
          "sources": [
              {"url": "https://pypi.org/", "verify_ssl": true},
          ]
       },
      "default": [
          {"name": "requests", "version": "0.11.2", "hash": "..."},
          {"name": "Django", "version": "1.6", "hash": "..."},
          {"name": "pinax", "git": "git://...", "ref": "1.4", "editable": true},
      ],
      "development": [
          {"name": "nose", "version": "1.3.7", "hash": "..."},
      ]
  }

Example Pip Integration (Eventually)
++++++++++++++++++++++++++++++++++++

Install packages from ``Pipfile``::
    
    $ pip install -p
    ! Warning: Pipfile.lock (48d35f) is out of date. Updating to (73d81f).
    Installing packages from Pipfile.lock...
    
    # Manually update lockfile.
    $ pip freeze -p Pipfile
    Pipfile.lock (73d81f) written to disk.
    
Notes::

    # -p accepts a path argument, which defaults to 'Pipfile'.
    # Pipfile.lock will be written automatically during `install -p` if it does not exist. 
    
Ideas::

- Resursively look for `Pipfile` in parent directories (limit 4?) when ``-p`` is bare. 
    

Useful Links
------------

- `pypa/pip#1795: Requirements 2.0 <https://github.com/pypa/pip/issues/1795>`_
- `Basic Concept Gist <https://gist.github.com/kennethreitz/4745d35e57108f5b766b8f6ff396de85>`_ (fork of @dstufft's)

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
