import json
import hashlib
import platform
from collections import OrderedDict


class PipfileParser(object):
    def __init__(self, filename='Pipfile'):
        self.filename = filename
        self.sources = []
        self.groups = OrderedDict({
            'default': [],
            'develop': []
        })
        self.group_stack = ['default']
        self.requirements = []

    def __repr__(self):
        return '<PipfileParser path={0!r}'.format(self.filename)

    def parse(self):
        with open(self.filename) as f:
            content = f.read()
        exec(content, {'__builtins__': None}, self.locals)
        data = OrderedDict({
            '_meta': {
                'sources': self.sources,
                'requires': self.requirements
            },
        })
        data.update(self.groups)
        return data

    @property
    def locals(self):
        return {
            'source': self.add_source,
            'package': self.add_package,
            'dev_package': self.add_dev_package,
            'requires': self.requires,
            'requires_python': self.requires_python,
            'True': True,
            'False': False,
        }

    def add_source(self, url, **kwargs):
        source = OrderedDict({'url': url})
        source.update(kwargs)
        self.sources.append(source)

    def add_package(self, name, version=None, **kwargs):
        package = OrderedDict()
        package['name'] = name
        if version:
            package['version'] = version
        package.update(kwargs)
        self.groups['default'].append(package)

    def add_dev_package(self, name, version=None, **kwargs):
        package = OrderedDict()
        package['name'] = name
        if version:
            package['version'] = version
        package.update(kwargs)
        self.groups['develop'].append(package)

    def requires(self, marker, specifier):
        requirement = OrderedDict()
        requirement['marker'] = marker
        requirement['specifier'] = specifier
        self.requirements.append(requirement)

    def requires_python(self, python_version):
        self.requires('python_version', python_version)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.group_stack.pop()


class Pipfile(object):
    def __init__(self, filename):
        super(Pipfile, self).__init__()
        self.filename = filename
        self.data = None

    @classmethod
    def load(klass, filename):
        p = PipfileParser(filename=filename)
        pipfile = klass(filename=filename)
        pipfile.data = p.parse()
        return pipfile

    @property
    def hash(self):
        return hashlib.sha256(self.contents).hexdigest()

    @property
    def contents(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def freeze(self):
        data = self.data
        data['_meta']['Pipfile-sha256'] = self.hash
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def assert_requirements(self):
        for requirement in self.data['_meta']['requires']:
            marker = requirement['marker']
            specifier = requirement['specifier']

            if marker == 'python_version':
                assert platform.python_version()[:3] == specifier


def load(pipfile_path):
    return Pipfile.load(filename=pipfile_path)