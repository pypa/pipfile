# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
from __future__ import absolute_import, division, print_function

import hashlib
import json

import pyrsistent


class Source(pyrsistent.PRecord):

    url = pyrsistent.field(type=str, mandatory=True)
    verify_ssl = pyrsistent.field(type=bool, initial=True, mandatory=True)


class Sources(pyrsistent.CheckedPVector):

    __type__ = Source


class Extras(pyrsistent.CheckedPVector):

    __type__ = str  # TODO: A better type for an Extra Name, or at least an invariant.


class Requirement(pyrsistent.PRecord):

    name = pyrsistent.field(type=str, mandatory=True)  # TODO: Invarient from packaging.
    version = pyrsistent.field(type=str)  # TODO: Invariant + factory for PEP 440 specifier
    extras = pyrsistent.field(type=Extras)

    # TODO: We need to handle things like git, urls, paths, etc.


class Requirements(pyrsistent.CheckedPVector):

    __type__ = Requirement


class Packages(pyrsistent.CheckedPMap):

    __key_type__ = str
    __value_type__ = Requirements

    def __invariant__(key, value):
        return (
            key in {"default", "development"},
            "Key must be one of 'default' or 'development'",
        )


class Pipfile(pyrsistent.PClass):

    sources = pyrsistent.field(type=Sources)
    packages = pyrsistent.field(type=Packages)

    # TODO: Handle PEP 508 environment markers

    def digests(self):
        # We need to compute the data in this Pipfile down into a hash
        # digest, this will ensure that we can detect the difference\
        # between two different Pipfiles based upon their *semantic*
        # differences not their byte differences.

        # First, we need to boil our Pipfile data down into something we
        # can hash, this is easy enough to do by just serializing it and
        # then dumping it to JSON in a deterministic way.
        content = json.dumps(
            self.serialize(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf8")

        # Now, we loop over our supported hashes, and we ensure that we
        # have a hash for all of them.
        digests = {
            hash_name: hashlib.new(hash_name, content).hexdigest().lower()
            for hash_name in {"sha256"}
        }

        # Finally, we turn it into a Digests object and we return it.
        return Digests.create(digests)

    def lock(self, *, sources, packages):
        # We need to compute the data in this Pipfile down into a hash digest,
        # this will ensure that our Pipfile.lock

        return PipfileLock.create({
            "digests": self.digests(),
            "sources": sources,
            "packages": packages,
        })


class Digests(pyrsistent.CheckedPMap):

    __key_type__ = str
    __value_type__ = str

    def __invariant__(key, value):
        return (
            key in {"sha256"},  # TODO: Do we *only* want to support sha256?
            "Key must be 'sha256'",
        )


class PipfileLock(pyrsistent.PClass):

    digests = pyrsistent.field(
        type=Digests,
        mandatory=True,
        invariant=lambda d: (len(d) > 0, "No digests"),
    )
    sources = pyrsistent.field(type=Sources)
    packages = pyrsistent.field(type=Packages)
