import json
import os
from unittest import TestCase, mock

from pipfile.api import PipfileParser


class TestEnvVarInsertion(TestCase):

    def setUp(self):
        self.p = PipfileParser()

    @staticmethod
    def example_dict(key):
        return {
            "a_string": "https://$%s@something.com" % key,
            "another_string": "https://${%s}@something.com" % key,
            "nested": {
                "a_string": "https://$%s@something.com" % key,
                "another_string": "${%s}" % key,
            },
            "list": [
                {
                    "a_string": "https://$%s@something.com" % key,
                    "another_string": "${%s}" % key,
                },
                {},
            ],
            "bool": True,
            "none": None,
        }

    @mock.patch.dict(os.environ, {'FOO': 'BAR'})
    def test_correctly_inserts_env_vars(self):
        parsed_dict = self.p.inject_environment_variables(self.example_dict('FOO'))

        self.assertEqual(parsed_dict["a_string"], "https://BAR@something.com")
        self.assertEqual(parsed_dict["another_string"], "https://BAR@something.com")
        self.assertEqual(parsed_dict["nested"]["another_string"], "BAR")
        self.assertEqual(parsed_dict["list"][0]["a_string"], "https://BAR@something.com")
        self.assertEqual(parsed_dict["list"][1], {})
        self.assertTrue(parsed_dict["bool"])
        self.assertIsNone(parsed_dict["none"])

    @mock.patch.dict(os.environ, {})
    def test_leaves_values_intact_if_no_var_exists(self):
        d = self.example_dict('FOO')

        raw = json.dumps(d)
        parsed = json.dumps(self.p.inject_environment_variables(d))

        self.assertEqual(raw, parsed)
