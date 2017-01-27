# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
from __future__ import absolute_import, division, print_function

import collections
import json
import os.path

import toml

from ._structures import Pipfile, PipfileLock


def _load_package(package, data):
    d = {}

    if isinstance(data, str):
        if data != "*":
            d["version"] = data
    else:
        d.update(data)

    # We put this last, because we don't want to allow a name field in the
    # actual data set to override the left most name.
    d["name"] = package

    return d


def _dump_package(package):
    name = package.pop("name")

    if len(package) == 1 and "version" in package:
        package = package["version"]
    elif not package:
        package = "*"

    return name, package


def loads(pipfile, lockfile=None):
    pipfile_data = {}
    for key, value in toml.loads(pipfile).items():
        if key == "source":
            pipfile_data["sources"] = value
        elif key == "packages":
            pipfile_data.setdefault("packages", {})["default"] = [_load_package(k, v) for k, v in value.items()]
        elif key == "dev-packages":
            pipfile_data.setdefault("packages", {})["development"] = [_load_package(k, v) for k, v in value.items()]
        elif key == "requires":
            pass
        else:
            raise ValueError("Unknown key {0!r}".format(key))

    pipfile_obj = Pipfile.create(pipfile_data)

    if lockfile is not None:
        lockfile_obj = PipfileLock.create(json.loads(lockfile))
    else:
        lockfile_obj = None

    return pipfile_obj, lockfile_obj


def load(pipfile_obj, lockfile_obj=None):
    return loads(
        pipfile_obj.read(),
        lockfile_obj.read() if lockfile_obj is not None else None,
    )


def dumps(obj):
    if isinstance(obj, Pipfile):
        data = collections.OrderedDict([
            ("source", obj.sources.serialize()),
            ("packages", dict(_dump_package(p) for p in obj.packages["default"].serialize())),
            ("dev-packages", dict(_dump_package(p) for p in obj.packages["development"].serialize())),
        ])
        return toml.dumps(data)
    elif isinstance(obj, PipfileLock):
        data = collections.OrderedDict([
            ("digests", obj.digests.serialize()),
            ("sources", obj.sources.serialize()),
            ("packages", obj.packages["default"].serialize()),
            ("dev-packages", obj.packages["development"].serialize()),
        ])
        return json.dumps(data, indent=4, separators=(",", ": "))
    else:
        raise ValueError("Unknown object type: {0!r}".format(obj.__class__))


def dump(file_obj, data):
    file_obj.write(dumps(data))


def find(root="."):
    # TODO: Use walk_up or something to actually recursively look upwards from
    #       the root directory instead of *only* looking in the root directory.
    # TODO: Also look for pipfile, Pipfile.toml, and pipfile.toml, in that
    #       order of preferece.
    pipfile_path = os.path.join(root, "Pipfile")
    if not os.path.exists(pipfile_path):
        return None, None

    with open(pipfile_path, "r", encoding="utf8") as pfp:
        # TODO: Also look for pipfile.lock.
        lockfile_path = os.path.join(
            os.path.dirname(pipfile_path),
            "Pipfile.lock",
        )
        if os.path.exists(lockfile_path):
            with open(lockfile_path, "r", encoding="utf8") as lfp:
                return load(pfp, lfp)
        else:
            return load(pfp)


def save(pipfile, pipfilelock=None, remove_stale=True, root="."):
    # TODO: Again we'd use walk_up or something here to attempt to recursively
    #       locate the files that we're going to be over-writing. Except this
    #       time if we couldn't find a file to replace, we'll just write new
    #       files in the root directory.
    pipfile_path = os.path.join(root, "Pipfile")
    lockfile_path = os.path.join(root, "Pipfile.lock")

    with open(pipfile_path, "w", encoding="utf8") as pfp:
        dump(pfp, pipfile)

    if pipfilelock is not None:
        with open(lockfile_path, "w", encoding="utf8") as lfp:
            dump(lfp, pipfilelock)
    elif remove_stale and os.path.exists(lockfile_path):
        os.remove(lockfile_path)
