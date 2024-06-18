"""import pytest
import yaml

from mapfbench.utils import dict_manipulations


class TestUtils:

    def test_dictionary_substitutions(self):
        list_associations = yaml.safe_load(open("C:\\Users\steve\PycharmProjects\mapfbench\src\mapfbench\\utils\default_associations.yaml"))

        associations = {}
        for association in list_associations:
            associations.update(association)

        dictionary = {
            "_avg_makespan": 1,
            "_plans": {
                "_plan_1": {
                    "_makespan": 10,
                    "_sum_of_costs": 20
                }
            }
        }

        new_dictionary = dict_manipulations.replace_from_prefixes(dictionary, associations)
        assert new_dictionary == {
            "Average Makespan": 1,
            "Plans": {
                "_plan_1": {
                   "_makespan": 10,
                   "_sum_of_costs": 20
                }
            }
        }

        new_dictionary = dict_manipulations.recursive_replace_from_prefixes(dictionary, associations)
        assert new_dictionary == {
            "Average Makespan": 1,
            "Plans": {
                "Plan_1": {
                    "Makespan": 10,
                    "Sum of costs": 20
                }
            }
        }
"""



