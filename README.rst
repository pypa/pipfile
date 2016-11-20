Pipfile
=======

**Warning**: this project is under active development.

A ``Pipfile`` is a new (and much better!) way to declare dependencies for your Python applications. It will be a full replacement for the well-pervasive `requirements.txt` files, currently installable with ``$ pip install -r``.

The Concept
-----------

A ``Pipfile`` will be superior to a ``requirements.txt`` file in a number of ways:

- Expressive Python syntax for declaring all types of Python dependencies.
- Grouping of sub-dependency groups (e.g. a ``testing`` group).
- Use of a single file only will be extremely encouraged.
- ``Pipfile.lock``


Example Pipfile
+++++++++++++++

Note—this is an evolving work in progress::

  # Note: There will be a default source, and context manager can also be used.
  source('https://pypi.org/', verify_ssl=True)

  dist('requests')
  dist('Django', '==1.6')
  dist('pinax', git='git://github.com/pinax/pinax.git', ref='1.4', editable=True)

  with group('development'):
    dist('nose')

Example Pipfile.lock
++++++++++++++++++++

Note—this file is always to be generated, not modified or constructed by a user::

  {
      "_meta": {
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
