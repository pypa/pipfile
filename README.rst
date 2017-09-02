Pipfile
=======

``Pipfile`` and its sister ``Pipfile.lock`` are a replacement for the existing standard `pip`_'s ``requirements.txt`` file. 

    WARNING: This project is under active design and development. Nothing is set in stone at this point of time.

This repository contains the design specification of the ``Pipfile`` format, as well as (soon) an implementation of a parser for the specification which can be used by `pip`_ and any other consumer, once the design (including the form of a ``Pipfile`` itself) has been built out and finalized.

.. _`pip`: https://pip.pypa.io/en/stable/


The Concept
-----------

``Pipfile`` will be superior to ``requirements.txt`` file in a number of ways:

* `TOML <https://github.com/toml-lang/toml>`_ syntax for declaring all types of Python dependencies.
* One Pipfile (as opposed to multiple ``requirements.txt`` files).

  * Existing requirements files tend to proliferate into multiple files - e.g. ``dev-requirements.txt``, ``test-requirements.txt``, etc. - but a ``Pipfile`` will allow seamlessly specifying groups of dependencies in one place.
  * This will be surfaced as only two built-in groups (*default* &     *development*). (see note below)

* Fully specified (and *deterministic*) environments in the form of ``Pipfile.lock``.
  A deployed application can then be completely redeployed with the same exact versions of all recursive dependencies, by referencing the ``Pipfile.lock`` file.

The concrete requirements for a Python Application would come from ``Pipfile``. This would include where the packages should be fetched from and their loose version constraints.

The details of the environment (all installed packages with pinned versions and other details) would be stored in ``Pipfile.lock``, for reproducibility. This file will be automatically generated and should not be modified by the user.

    NOTE: Custom groups may be added in the future. Remember, it is easier to add features in the future than it is to remove them.

    The Composer community has been successful with only *default* and *development* as group options for many years. This model would be tried/followed at first.


Examples
--------

    NOTE: This is an evolving work in progress.

``Pipfile``
+++++++++++

.. code-block:: toml

    [[source]]
    url = 'https://pypi.python.org/simple'
    verify_ssl = true

    [requires]
    python_version = '2.7'

    [packages]
    requests = { extras = ['socks'] }
    records = '>0.5.0'
    django = { git = 'https://github.com/django/django.git', ref = '1.11.4', editable = true }

    [dev-packages]
    nose = '*'

Notes:

- There will be a default ``source``.

**PEP 508 Support** 
+++++++++++++++++++

.. code-block:: toml

    # Support for all PEP 508 markers
    [requires]
    python_full_version = '3.6.0b1'

    platform = 'windows'

``requires`` utilizes  `PEP 508`_ ``marker =  'specifier'`` markers. This functionality may not be readily used, as it is only to assert (and therefore abort, if appropriate) installation on certain platforms (e.g. python version, platform version).

.. _`PEP 508`: https://www.python.org/dev/peps/pep-0508/#environment-markers

``Pipfile.lock``
++++++++++++++++

.. code-block:: json

    {
        "_meta": {
            "hash": {
                "sha256": "b6d9e4a95bcb62207883a8f0ea52261650017e6c50b7aa01e112111a99fd298a"
            },
            "pipfile-spec": 1,
            "requires": {
                "python_version": "2.7"
            },
            "sources": [
                {
                    "url": "https://pypi.python.org/simple",
                    "verify_ssl": true
                }
            ]
        },
        "default": {
            "certifi": {
                "version": "==2017.7.27.1"
            },
            "chardet": {
                "version": "==3.0.4"
            },
            "django": {
                "editable": true,
                "git": "https://github.com/django/django.git",
                "ref": "1.11.4"
            },
            "docopt": {
                "version": "==0.6.2"
            },
            "et-xmlfile": {
                "version": "==1.0.1"
            },
            "idna": {
                "version": "==2.6"
            },
            "jdcal": {
                "version": "==1.3"
            },
            "numpy": {
                "version": "==1.13.1"
            },
            "odfpy": {
                "version": "==1.3.5"
            },
            "openpyxl": {
                "version": "==2.4.8"
            },
            "pandas": {
                "version": "==0.20.3"
            },
            "pysocks": {
                "version": "==1.6.7"
            },
            "python-dateutil": {
                "version": "==2.6.1"
            },
            "pytz": {
                "version": "==2017.2"
            },
            "pyyaml": {
                "version": "==3.12"
            },
            "records": {
                "version": "==0.5.1"
            },
            "requests": {
                "version": "==2.18.4"
            },
            "six": {
                "version": "==1.10.0"
            },
            "sqlalchemy": {
                "version": "==1.1.13"
            },
            "tablib": {
                "version": "==0.12.1"
            },
            "unicodecsv": {
                "version": "==0.14.1"
            },
            "urllib3": {
                "version": "==1.22"
            },
            "xlrd": {
                "version": "==1.1.0"
            },
            "xlwt": {
                "version": "==1.3.0"
            }
        },
        "develop": {
            "nose": {
                "version": "==1.3.7"
            }
        }
    }

``Pipfile.lock`` is always to be generated and is not to be modified or constructed by a user.

Do note how the versions of each dependency are recursively frozen and a hash gets computed so that you can take advantage of `new pip security features`_

.. _`new pip security features`: https://pip.pypa.io/en/stable/reference/pip_install/#hash-checking-mode

Pip Integration (eventual)
++++++++++++++++++++++++++

`pip`_ will grow a new command line option, ``-p`` / ``--pipfile`` to install the versions as specified in a ``Pipfile``, similar to its existing ``-r`` / ``--requirement`` argument for installing ``requirements.txt`` files.

Install packages from ``Pipfile``::

    $ pip install -p
    ! Warning: Pipfile.lock (48d35f) is out of date. Updating to (73d81f).
    Installing packages from requirements.piplock...
    [installation output]

To manually update the ``Pipfile.lock``::

    $ pip freeze -p different_pipfile
    different_pipfile.lock (73d81f) written to disk.

Notes::

    # -p accepts a path argument, which defaults to 'Pipfile'.
    # Pipfile.lock will be written automatically during `install -p` if it does not exist.

Ideas::

- Recursively look for `Pipfile` in parent directories (limit 3/4?) when ``-p`` is bare.


Useful Links
------------

- `pypa/pip#1795`_: Requirements 2.0
- `Basic Concept Gist`_ (fork of @dstufft's)

.. _`Basic Concept Gist`: https://gist.github.com/kennethreitz/4745d35e57108f5b766b8f6ff396de85
.. _`pypa/pip#1795`: https://github.com/pypa/pip/issues/1795

Inspirations
++++++++++++

- `nvie/pip-tools`_: A set of tools to keep your pinned Python dependencies fresh.
- `A Better Pip Workflow`_ by Kenneth Reitz
- Lessons learned from Composer, Cargo, Yarn, NPM, Bundler and friends.

.. _`nvie/pip-tools`: https://github.com/nvie/pip-tools
.. _`A Better Pip Workflow`: https://www.kennethreitz.org/essays/a-better-pip-workflow


Documentation
-------------

The `documentation`_ for this project will, eventually, reside at pypi.org.

.. _`documentation`: https://pipfile.pypa.io/


Discussion
----------

If you run into bugs, you can file them in our `issue tracker`_. You can also join ``#pypa`` on Freenode to ask questions or get involved.

.. _`issue tracker`: https://github.com/pypa/pipfile/issues


Code of Conduct
---------------

Everyone interacting in the pipfile project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
