Pipfile
=======

**Warning**: this project is under active development. 

A ``Pipfile`` is a new (and much better!) way to declare dependencies for your Python applications. It will be a full replacement for the well-pervasive `requirements.txt` files, currently installable with ``$ pip install -r``.

The Concept
-----------

A ``Pipfile`` will be superior to a ``requirements.txt`` file in a number of ways:

- Expressive Python syntax for declaring all types of Python dependencies. 
- Grouping of sub-dependency groups (e.g. a ``testing`` group)
- Use of a single file only will be extremely encouraged.
- ``Pipfile.lock``


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
