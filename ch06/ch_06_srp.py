"""S.O.L.I.D Design.

Chapter 6. SRP.
"""

# 06_01

class Simulator:
    def __init__(self, house, player):
        pass
    def run(self):
        pass
    @property
    def final_stats(self):
        pass

# 06_02

import pathlib

class StatsDB:
    def __init__(self, path):
        self.path= path
    def dump(self, stats_document):
        pass

import json

class JSONStatsDB(StatsDB):
    def dump(self, stats_document):
        with self.path.open('w') as target:
            json.dump(stats_document, target, indent=2)

import yaml

class YAMLStatsDB(StatsDB):
    def dump(self, stats_document):
        with self.path.open('w') as target:
            yaml.dump(stats_document, target, indent=2, default_flow_style=False)

def output_factory(parameter, path) -> StatsDB:
    if parameter == "JSON":
        return JSONStatsDB(path)
    elif parameter == "YAML":
        return YAMLStatsDB(path)
    else:
        raise ValueError("Unknown format")

__test__ = {
    'JSONStatsDB': '''
>>> data = {'wins': 11, 'loses': 13}
>>> path = pathlib.Path("stats.json")
>>> db = JSONStatsDB(path)
>>> db.dump(data)
>>> with path.open() as test:
...     saved = json.load(test)
>>> data == saved
True
>>> path.unlink()
''',

    'YAMLStatsDB': '''
>>> data = {'wins': 17, 'loses': 19}
>>> path = pathlib.Path("stats.yaml")
>>> db = YAMLStatsDB(path)
>>> db.dump(data)
>>> with path.open() as test:
...     saved = yaml.load(test)
>>> data == saved
True
>>> path.unlink()
''',


    'factory': '''
>>> data = {'wins': 23, 'loses': 29}
>>> path = pathlib.Path("stats.yaml")
>>> db = output_factory("JSON", path)
>>> db.dump(data)
>>> with path.open() as test:
...     saved = json.load(test)
>>> data == saved
True
>>> path.unlink()
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
