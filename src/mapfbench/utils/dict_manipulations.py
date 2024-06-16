import pathlib
from typing import Any

import yaml


def replace_key(dictionary: dict, old_key: Any, new_key: Any):
    try:
        dictionary[new_key] = dictionary.pop(old_key)
    except KeyError:
        return


def replace_from_association(dictionary: dict[str, Any], associations: dict[str, str]):
    for association in associations.items():
        replace_key(dictionary, association[0], association[1])


def replace_from_prefixes(dictionary: dict[str, Any], associations: dict[str, str]):
    prefixes = tuple(associations.keys())
    new_dict = dictionary.copy()
    for key in dictionary:
        prefix = [x for x in prefixes if key.startswith(x)]
        if len(prefix) > 0:
            prefix = prefix[0]
            remaining = key.removeprefix(prefix)
            replace_key(new_dict, key, associations[prefix] + remaining)

    return new_dict


def recursive_replace_from_prefixes(dictionary: dict[str, Any], associations: dict[str, str]):
    new_dict = replace_from_prefixes(dictionary, associations)
    for key, value in new_dict.items():
        if isinstance(value, dict):
            new_dict[key] = recursive_replace_from_prefixes(new_dict[key], associations)

    return new_dict


def get_associations():
    path = pathlib.Path(__file__).parent.absolute() / 'default_associations.yaml'
    list_associations = yaml.safe_load(
        open(path))
    new_associations = {}
    for association in list_associations:
        new_associations.update(association)
    return new_associations


def use_readable_prefixes(dictionary: dict[str, Any]):
    return recursive_replace_from_prefixes(dictionary, get_associations())
