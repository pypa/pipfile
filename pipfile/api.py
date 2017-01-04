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

    def __repr__(self):
        return '<PipfileParser path={0!r}'.format(self.filename)

    def parse(self):
        with open(self.filename) as f:
            content = f.read()
        exec(content, {'__builtins__': None}, self.locals)
        data = OrderedDict({
            '_meta': {
                'sources': self.sources,
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
            'group': self.set_group,
            'True': True,
            'False': False,
        }

    def add_source(self, url, **kwargs):
        source = OrderedDict({'url': url})
        source.update(kwargs)
        self.sources.append(source)

    @property
    def current_group(self):
        return self.group_stack[-1]

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

    def set_group(self, name):
        self.group_stack.append(name)
        self.groups[name] = []
        return self

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.group_stack.pop()


class Pipfile(object):
    def __init__(self,):
        super(Pipfile, self).__init__()
        self.filename = None

    @classmethod
    def load(klass, filename):
        pass


def load(pipfile_path):
    p = PipfileParser(filename=pipfile_path)
    return p.parse()

def function():
    pass