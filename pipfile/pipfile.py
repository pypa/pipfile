from collections import OrderedDict


class Pipfile(object):
    def __init__(self, filename='Pipfile'):
        self.filename = filename
        self.sources = []
        self.groups = OrderedDict({
            'default': []
        })
        self.group_stack = ['default']

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
        self.groups[self.current_group].append(package)

    def set_group(self, name):
        self.group_stack.append(name)
        self.groups[name] = []
        return self

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.group_stack.pop()

