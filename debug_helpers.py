from typing import Dict, Any
import json



def compare_nested_objects(old: Any, new: Any) -> bool:
    """
    Compares two nested objects to check if they are the same. The function recursively iterates over elements if the objects are list or dict.

    Args:
        old (Any): The first object to compare.
        new (Any): The second object to compare.

    Returns:
        bool: True if objects are the same, False otherwise.
    """
    if type(old) != type(new):
        return False

    if isinstance(old, dict):
        for key in old:
            if key not in new or not compare_nested_objects(old[key], new[key]):
                return False
        return True

    elif isinstance(old, list):
        if len(old) != len(new):
            return False
        for item_old, item_new in zip(old, new):
            if not compare_nested_objects(item_old, item_new):
                return False
        return True

    else:
        return old == new


def generate_diff(old_state: Dict, new_state: Dict) -> str:
    """
    Generates a difference between two dictionaries. The function checks for changes in the dictionary values and
    stores the differences in two separate dictionaries for old and new states. The function can handle nested dictionaries.

    Args:
        old_state (Dict): The old state dictionary.
        new_state (Dict): The new state dictionary.

    Returns:
        str: A JSON string representing the differences between old and new states. The JSON object has two keys 'old' and 'new'
        containing the differences in old and new states respectively.
    """
    old_diff = {}
    new_diff = {}

    for key in new_state:
        if key not in old_state or not compare_nested_objects(old_state[key], new_state[key]):
            if isinstance(old_state[key], dict) and isinstance(new_state[key], dict):
                sub_old_diff = {k: old_state[key][k] for k in new_state[key] if k not in old_state[key] or old_state[key][k] != new_state[key][k]}
                sub_new_diff = {k: new_state[key][k] for k in new_state[key] if k not in old_state[key] or old_state[key][k] != new_state[key][k]}
                if sub_old_diff:
                    old_diff[key] = sub_old_diff
                if sub_new_diff:
                    new_diff[key] = sub_new_diff
            else:
                old_diff[key] = old_state[key]
                new_diff[key] = new_state[key]

    return json.dumps({'old': old_diff, 'new': new_diff}, indent=2, default=str)
