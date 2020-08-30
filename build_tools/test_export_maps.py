"""
Wrote a deep merge function for funz, and easier to test with tests
"""

import unittest
import six

six.add_move(six.MovedModule('mock', 'mock', 'unittest.mock'))
from six.moves import mock

with mock.patch.dict('sys.modules', {'gimpfu': mock.Mock()}):
    import export_maps

class TestMerge(unittest.TestCase):

    D1 = {
        'a': 2,
        'b': [{'a': 2, 'b': 4}, 6, [0, 2, 6], 8],
        'c': [{'a': 2, 'b': 4}, 6, [0, 2, 6], 8],
        '1': 8,
        '2': {'f': [[2], 4, {'a': 2}], 'c': 4, 'b': 'a'},
        '3': 16,
    }

    D2 = {
        'b': [{'c': 1, 'b': 5}, 3, [1, 7, 3], 5],
        'd': 3,
        '2': {'f': [[1], 3, {'a': 5}], 'b': 3},
        'f': [{'a': 3, 'b': 41}, 3, [1, 7, 3], 5],
        'g': 13,
        '3': 5,
        '71/2': 13,
    }

    D1_D2 = {
        'a': 2,
        'b': [{'a': 2, 'c': 1, 'b': 5}, 6, [0, 2, 6, 1, 7, 3], 8, 3, 5],
        'c': [{'a': 2, 'b': 4}, 6, [0, 2, 6], 8],
        'd': 3,
        'f': [{'a': 3, 'b': 41}, 3, [1, 7, 3], 5],
        'g': 13,
        '1': 8,
        '2': {'f': [[2, 1], 4, {'a': 5}, 3], 'c': 4, 'b': 3},
        '3': 5,
        '71/2': 13
    }

    def test(self):

        self.assertEqual(export_maps._merge(self.D1, self.D2), self.D1_D2)
