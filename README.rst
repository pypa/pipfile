Pipfile: the replacement for `requirements.txt`
===============================================

``Pipfile`` and its sister ``Pipfile.lock`` are designed as a proposed replacement for an existing format: `pip`_'s ``requirements.txt`` file.

    WARNING: This format is still under active design and development. Nothing is set in stone at this point in time.

This repository contains the design specification of the ``Pipfile`` format, as well as a proposed implementation of a parser for the specification which can be used by `Pipenv`_ and, in the future, any other consumer (e.g. `pip`_), once the design (including the form of a ``Pipfile`` itself) has been built out and finalized.

.. _`pip`: https://pip.pypa.io/en/stable/
.. _`pipenv`: https://pipenv.pypa.io/en/stable/

-------------------------

Today, `Pipenv <https://pipenv.pypa.io/en/stable/>`_ uses Pipfile and contains the current reference implementation.

The Concept
-----------

``Pipfile`` will be superior to ``requirements.txt`` file in a number of ways:

* `TOML <https://github.com/toml-lang/toml>`_ syntax for declaring all types of Python dependencies.
* One ``Pipfile`` (as opposed to multiple ``requirements.txt`` files).

* A ``Pipfile`` is inherently ordered.

* Existing requirements files tend to proliferate into multiple files - e.g. ``dev-requirements.txt``, ``test-requirements.txt``, etc. - but a ``Pipfile`` will allow seamlessly specifying groups of dependencies in one place.
  * This will be surfaced as only two built-in groups (*default* &     *development*). (see note below)

* Fully specified (and *deterministic*) environments in the form of ``Pipfile.lock``.
  A deployed application can then be completely redeployed with the same exact versions of all recursive dependencies, by referencing the ``Pipfile.lock`` file.

The concrete requirements for a Python Application would come from ``Pipfile``. This would include where the packages should be fetched from and their loose version constraints.

The details of the environment (all installed packages with pinned versions and other details) would be stored in ``Pipfile.lock``, for reproducibility. This file will be automatically generated and should not be modified by the user.

.. note:: Custom groups may be added in the future. Remember, it is easier to add features in the future than it is to remove them. The Composer community has been successful with only *default* and *development* as group options for many years. This model is being followed.


Examples (spec v6)
------------------

Here is a complex, comprehensive example ``Pipfile`` and the resulting ``Pipfile.lock``, generated with `Pipenv <http://pipenv.org>`_, and this library:

``Pipfile``
+++++++++++

.. code-block:: toml

    [[source]]
    url = 'https://pypi.python.org/simple'
    verify_ssl = true
    name = 'pypi'

    [requires]
    python_version = '2.7'

    [packages]
    requests = { extras = ['socks'] }
    records = '>0.5.0'
    django = { git = 'https://github.com/django/django.git', ref = '1.11.4', editable = true }
    "e682b37" = {file = "https://github.com/divio/django-cms/archive/release/3.4.x.zip"}
    "e1839a8" = {path = ".", editable = true}
    pywinusb = { version = "*", os_name = "=='nt'", index="pypi"}

    [dev-packages]
    nose = '*'
    unittest2 = {version = ">=1.0,<3.0", markers="python_version < '2.7.9' or (python_version >= '3.0' and python_version < '3.4')"}

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

This functionality can currently be tested with ``$ pipenv check``.

.. _`PEP 508`: https://www.python.org/dev/peps/pep-0508/#environment-markers

``Pipfile.lock``
++++++++++++++++

.. code-block:: json

    {
        "_meta": {
            "hash": {
                "sha256": "09da36fcc93fa9b94fbea5282d8206a9d2e13fcec27229ec62c16c134e3e760a"
            },
            "host-environment-markers": {
                "implementation_name": "cpython",
                "implementation_version": "0",
                "os_name": "posix",
                "platform_machine": "x86_64",
                "platform_python_implementation": "CPython",
                "platform_release": "17.0.0",
                "platform_system": "Darwin",
                "platform_version": "Darwin Kernel Version 17.0.0: Thu Aug 24 21:48:19 PDT 2017; root:xnu-4570.1.46~2/RELEASE_X86_64",
                "python_full_version": "2.7.14",
                "python_version": "2.7",
                "sys_platform": "darwin"
            },
            "pipfile-spec": 6,
            "requires": {
                "python_version": "2.7"
            },
            "sources": [
                {
                    "name": "pypi",
                    "url": "https://pypi.python.org/simple",
                    "verify_ssl": true
                }
            ]
        },
        "default": {
            "certifi": {
                "hashes": [
                    "sha256:54a07c09c586b0e4c619f02a5e94e36619da8e2b053e20f594348c0611803704",
                    "sha256:40523d2efb60523e113b44602298f0960e900388cf3bb6043f645cf57ea9e3f5"
                ],
                "version": "==2017.7.27.1"
            },
            "chardet": {
                "hashes": [
                    "sha256:fc323ffcaeaed0e0a02bf4d117757b98aed530d9ed4531e3e15460124c106691",
                    "sha256:84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"
                ],
                "version": "==3.0.4"
            },
            "django": {
                "editable": true,
                "git": "https://github.com/django/django.git",
                "ref": "1.11.4"
            },
            "docopt": {
                "hashes": [
                    "sha256:49b3a825280bd66b3aa83585ef59c4a8c82f2c8a522dbe754a8bc8d08c85c491"
                ],
                "version": "==0.6.2"
            },
            "e1839a8": {
                "editable": true,
                "path": "."
            },
            "e682b37": {
                "file": "https://github.com/divio/django-cms/archive/release/3.4.x.zip"
            },
            "et-xmlfile": {
                "hashes": [
                    "sha256:614d9722d572f6246302c4491846d2c393c199cfa4edc9af593437691683335b"
                ],
                "version": "==1.0.1"
            },
            "idna": {
                "hashes": [
                    "sha256:8c7309c718f94b3a625cb648ace320157ad16ff131ae0af362c9f21b80ef6ec4",
                    "sha256:2c6a5de3089009e3da7c5dde64a141dbc8551d5b7f6cf4ed7c2568d0cc520a8f"
                ],
                "version": "==2.6"
            },
            "jdcal": {
                "hashes": [
                    "sha256:b760160f8dc8cc51d17875c6b663fafe64be699e10ce34b6a95184b5aa0fdc9e"
                ],
                "version": "==1.3"
            },
            "lxml": {
                "hashes": [
                    "sha256:3593f49858fc6229cd93326be06b099ae477fd65d8f4a981320a6d0bb7fc7a5a",
                    "sha256:8996df6b0f205b00b89bbd04d88f1fa1e04139a025fd291aa4ddd05dc86836f4",
                    "sha256:9f399c37b8e61c3989ef12ecf0abd9c10a5075f0fc9ad1ecd67ce6f9c72a7211",
                    "sha256:550a51dee73c14e5863bdbbbe5836b2b8092a3f92631b5a908b9c41e72f123a5",
                    "sha256:e37eda3d05519918403084b43eb7324df21a0daf45c8ae8172a860710dd0fa78",
                    "sha256:48ab0e79175fd16f9478edc679ee14c79524c64b26f665f92cbecff81312d04d",
                    "sha256:52e18dd86f153c4383bb4c4ef62f81f9b7e44809d068848a5a183b2285496faf",
                    "sha256:0b8f3d6e669ea26849a6184f04c7802dbef6fd418a8b90e6c026e237db07af31",
                    "sha256:567b76f291a8d02aa8b4d3f8295ae749ac4d532570d8a8c7176f0556c7d95891",
                    "sha256:61825daaf2d80dc3da7635ee108720b0739962db008343822753bbf343cbfd14",
                    "sha256:b7f6ef610680709be11cb7662e46e254bc561dafe0de3b4848be2cf3924bd300",
                    "sha256:824664493a012f5b70396e841a4b4049bdaf445a70307e60f82fe35619f72cc7",
                    "sha256:e908d685800626f10cd6ae01a013fc42094be167fb2a683eb920dfddfaa0ee76",
                    "sha256:10c86b2248043f4428be33ed10202764b02b281eaa4550f16f0fbbc6ccaae9ac",
                    "sha256:d9ec728caddb161405e7c33ed9d176e96309893481370163bbf4b00e43008795",
                    "sha256:b2ecb3fd5470b740dfc21b064bbc1337be4b7b805994a868488145d36f35f517",
                    "sha256:a211288459c9115ddb255ff88e8ac12dc2063e70bddc15e3c65136477a358bb5",
                    "sha256:1f81074e77c25f9b787fa3854f400ca924d3d798cb7ae910c0e7920be7138c90",
                    "sha256:99b7eabfb46663ed5918eca4ed12420613ba24196964a741ccd962d09296c0b2",
                    "sha256:a8ad0adeedbbb7b85916214fcd4f5d02829d0e7b3c32abc298789218b6c3d699",
                    "sha256:88d137e440b5de35df2e0616da8e28a88d0119abdaa84520ad1ba815ee9da732",
                    "sha256:c4e02657e629f02ab8712471d77d6896c2cf6f09f8ffa6a0f23b1b1ef0318474",
                    "sha256:9581b438e5d0d0a6fa3937fac2abffd95380bd513bcd39f6952bfcf20cf0b9a7",
                    "sha256:c446fde3284c363cd2085ad1ce5a07c18f15f6766d72684622bc14b0a9ddfd29",
                    "sha256:d4507916c408feec2ea8cee3f0d1380e49ea431f6e07b0dd927388bd6e92d6eb",
                    "sha256:7030f44b758e930fd09ade87d770f5a231a19a8c561a3acc54e5122b5ec09e29",
                    "sha256:d78c0a114cf127a41a526aef99aef539c0b2537e57f04a2cc7a49e2c94a44ab8",
                    "sha256:f7bc9f702500e205b1560d620f14015fec76dcd6f9e889a946a2ddcc3c344fd0"
                ],
                "version": "==4.0.0"
            },
            "odfpy": {
                "hashes": [
                    "sha256:6db9bb1c9ea2d55d60e508a1318fd285442a8342b785704ea08598a260875a83",
                    "sha256:6f8163f8464868cff9421a058f25566e41d73c8f7e849c021b86630941b44366"
                ],
                "version": "==1.3.5"
            },
            "openpyxl": {
                "hashes": [
                    "sha256:ee7551efb70648fa8ee569c2b6a6dbbeff390cc94b321da5d508a573b90a4f17"
                ],
                "version": "==2.4.8"
            },
            "pysocks": {
                "hashes": [
                    "sha256:18842328a4e6061f084cfba70f6950d9140ecf7418b3df7cef558ebb217bac8d",
                    "sha256:d00329f27efa157db7efe3ca26fcd69033cd61f83822461ee3f8a353b48e33cf"
                ],
                "version": "==1.6.7"
            },
            "pytz": {
                "hashes": [
                    "sha256:c883c2d6670042c7bc1688645cac73dd2b03193d1f7a6847b6154e96890be06d",
                    "sha256:03c9962afe00e503e2d96abab4e8998a0f84d4230fa57afe1e0528473698cdd9",
                    "sha256:487e7d50710661116325747a9cd1744d3323f8e49748e287bc9e659060ec6bf9",
                    "sha256:43f52d4c6a0be301d53ebd867de05e2926c35728b3260157d274635a0a947f1c",
                    "sha256:d1d6729c85acea5423671382868627129432fba9a89ecbb248d8d1c7a9f01c67",
                    "sha256:54a935085f7bf101f86b2aff75bd9672b435f51c3339db2ff616e66845f2b8f9",
                    "sha256:39504670abb5dae77f56f8eb63823937ce727d7cdd0088e6909e6dcac0f89043",
                    "sha256:ddc93b6d41cfb81266a27d23a79e13805d4a5521032b512643af8729041a81b4",
                    "sha256:f5c056e8f62d45ba8215e5cb8f50dfccb198b4b9fbea8500674f3443e4689589"
                ],
                "version": "==2017.2"
            },
            "pywinusb": {
                "hashes": [
                    "sha256:e2f5e89f7b74239ca4843721a9bda0fc99014750630c189a176ec0e1b35e86df"
                ],
                "index": "pypi",
                "markers": "os_name == 'nt'",
                "version": "==0.4.2"
            },
            "pyyaml": {
                "hashes": [
                    "sha256:3262c96a1ca437e7e4763e2843746588a965426550f3797a79fca9c6199c431f",
                    "sha256:16b20e970597e051997d90dc2cddc713a2876c47e3d92d59ee198700c5427736",
                    "sha256:e863072cdf4c72eebf179342c94e6989c67185842d9997960b3e69290b2fa269",
                    "sha256:bc6bced57f826ca7cb5125a10b23fd0f2fff3b7c4701d64c439a300ce665fff8",
                    "sha256:c01b880ec30b5a6e6aa67b09a2fe3fb30473008c85cd6a67359a1b15ed6d83a4",
                    "sha256:827dc04b8fa7d07c44de11fabbc888e627fa8293b695e0f99cb544fdfa1bf0d1",
                    "sha256:592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab",
                    "sha256:5f84523c076ad14ff5e6c037fe1c89a7f73a3e04cf0377cb4d017014976433f3",
                    "sha256:0c507b7f74b3d2dd4d1322ec8a94794927305ab4cebbe89cc47fe5e81541e6e8",
                    "sha256:b4c423ab23291d3945ac61346feeb9a0dc4184999ede5e7c43e1ffb975130ae6",
                    "sha256:ca233c64c6e40eaa6c66ef97058cdc80e8d0157a443655baa1b2966e812807ca",
                    "sha256:4474f8ea030b5127225b8894d626bb66c01cda098d47a2b0d3429b6700af9fd8",
                    "sha256:326420cbb492172dec84b0f65c80942de6cedb5233c413dd824483989c000608",
                    "sha256:5ac82e411044fb129bae5cfbeb3ba626acb2af31a8d17d175004b70862a741a7"
                ],
                "version": "==3.12"
            },
            "records": {
                "hashes": [
                    "sha256:6d060a2b44ecc198d4e86efd5dab8558a2581b4019970bd8839e1604a243f57e",
                    "sha256:238cba35e8efbb724493bbb195bd027d9e78db4a978597969a7af0f722ac3686"
                ],
                "version": "==0.5.2"
            },
            "requests": {
                "hashes": [
                    "sha256:6a1b267aa90cac58ac3a765d067950e7dbbf75b1da07e895d1f594193a40a38b",
                    "sha256:9c443e7324ba5b85070c4a818ade28bfabedf16ea10206da1132edaa6dda237e"
                ],
                "version": "==2.18.4"
            },
            "sqlalchemy": {
                "hashes": [
                    "sha256:f1191e29e35b6fe1aef7175a09b1707ebb7bd08d0b17cb0feada76c49e5a2d1e"
                ],
                "version": "==1.1.14"
            },
            "tablib": {
                "hashes": [
                    "sha256:b8cf50a61d66655229993f2ee29220553fb2c80403479f8e6de77c0c24649d87"
                ],
                "version": "==0.12.1"
            },
            "unicodecsv": {
                "hashes": [
                    "sha256:018c08037d48649a0412063ff4eda26eaa81eff1546dbffa51fa5293276ff7fc"
                ],
                "version": "==0.14.1"
            },
            "urllib3": {
                "hashes": [
                    "sha256:06330f386d6e4b195fbfc736b297f58c5a892e4440e54d294d7004e3a9bbea1b",
                    "sha256:cc44da8e1145637334317feebd728bd869a35285b93cbb4cca2577da7e62db4f"
                ],
                "version": "==1.22"
            },
            "xlrd": {
                "hashes": [
                    "sha256:83a1d2f1091078fb3f65876753b5302c5cfb6a41de64b9587b74cefa75157148",
                    "sha256:8a21885513e6d915fe33a8ee5fdfa675433b61405ba13e2a69e62ee36828d7e2"
                ],
                "version": "==1.1.0"
            },
            "xlwt": {
                "hashes": [
                    "sha256:a082260524678ba48a297d922cc385f58278b8aa68741596a87de01a9c628b2e",
                    "sha256:c59912717a9b28f1a3c2a98fd60741014b06b043936dcecbc113eaaada156c88"
                ],
                "version": "==1.3.0"
            }
        },
        "develop": {
            "argparse": {
                "hashes": [
                    "sha256:c31647edb69fd3d465a847ea3157d37bed1f95f19760b11a47aa91c04b666314",
                    "sha256:62b089a55be1d8949cd2bc7e0df0bddb9e028faefc8c32038cc84862aefdd6e4"
                ],
                "version": "==1.4.0"
            },
            "linecache2": {
                "hashes": [
                    "sha256:e78be9c0a0dfcbac712fe04fbf92b96cddae80b1b842f24248214c8496f006ef",
                    "sha256:4b26ff4e7110db76eeb6f5a7b64a82623839d595c2038eeda662f2a2db78e97c"
                ],
                "version": "==1.0.0"
            },
            "nose": {
                "hashes": [
                    "sha256:dadcddc0aefbf99eea214e0f1232b94f2fa9bd98fa8353711dacb112bfcbbb2a",
                    "sha256:9ff7c6cc443f8c51994b34a667bbcf45afd6d945be7477b52e97516fd17c53ac",
                    "sha256:f1bffef9cbc82628f6e7d7b40d7e255aefaa1adb6a1b1d26c69a8b79e6208a98"
                ],
                "version": "==1.3.7"
            },
            "six": {
                "hashes": [
                    "sha256:832dc0e10feb1aa2c68dcc57dbb658f1c7e65b9b61af69048abc87a2db00a0eb",
                    "sha256:70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9"
                ],
                "version": "==1.11.0"
            },
            "traceback2": {
                "hashes": [
                    "sha256:8253cebec4b19094d67cc5ed5af99bf1dba1285292226e98a31929f87a5d6b23",
                    "sha256:05acc67a09980c2ecfedd3423f7ae0104839eccb55fc645773e1caa0951c3030"
                ],
                "version": "==1.4.0"
            },
            "unittest2": {
                "hashes": [
                    "sha256:13f77d0875db6d9b435e1d4f41e74ad4cc2eb6e1d5c824996092b3430f088bb8",
                    "sha256:22882a0e418c284e1f718a822b3b022944d53d2d908e1690b319a9d3eb2c0579"
                ],
                "markers": "python_version < '2.7.9' or (python_version >= '3.0' and python_version < '3.4')",
                "version": "==1.1.0"
            }
        }
    }



This `example <https://github.com/pypa/pipfile/tree/master/examples>`_ was generated with ``$ pipenv lock``.

``Pipfile.lock`` is always to be generated and is not to be modified or constructed by a user.

Do note how the versions of each dependency are recursively frozen and a hash gets computed so that you can take advantage of `new pip security features`_.

Hashes are optional, because they can cause problems when using the same lockfile across different Python versions (e.g. a package will have different hashes according to different Pythons).

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

- `Pipenv`_: Current reference implementation
- `pypa/pip#1795`_: Requirements 2.0
- `Basic Concept Gist`_ (fork of @dstufft's)

.. _`Pipenv`: http://pipenv.org
.. _`Basic Concept Gist`: https://gist.github.com/kennethreitz/4745d35e57108f5b766b8f6ff396de85
.. _`pypa/pip#1795`: https://github.com/pypa/pip/issues/1795

Inspirations
++++++++++++

- `nvie/pip-tools`_: A set of tools to keep your pinned Python dependencies fresh.
- `A Better Pip Workflow`_ by Kenneth Reitz
- Lessons learned from Composer, Cargo, Yarn, NPM, Bundler and all Languages Owners at Heroku.


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

Everyone interacting in the pipfile project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the `PSF Code of Conduct`_.

.. _`PSF Code of Conduct`: https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md
