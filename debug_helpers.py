from typing import Dict, Any
from tangerine import Ctx
import json


# def generate_diff(old_state: Dict, new_state: Dict) -> str:
#     diff = {}
#     for key in new_state:
#         if key != 'socket' and (key not in old_state or old_state[key] != new_state[key]):
#             diff[key] = new_state[key]

#     return json.dumps(diff, indent=2, default=str)

# def copy_context_without_socket(ctx: Ctx) -> Dict:
#     ctx_copy = vars(ctx).copy()
#     ctx_copy.pop('socket', None)
#     return ctx_copy


# def compare_nested_objects(old: Any, new: Any) -> bool:
#     if type(old) != type(new):
#         return False

#     if isinstance(old, dict):
#         for key in old:
#             if key not in new or not compare_nested_objects(old[key], new[key]):
#                 return False
#         return True

#     elif isinstance(old, list):
#         if len(old) != len(new):
#             return False
#         for item_old, item_new in zip(old, new):
#             if not compare_nested_objects(item_old, item_new):
#                 return False
#         return True

#     else:
#         return old == new

# def generate_diff(old_state: Dict, new_state: Dict) -> str:
#     diff = {}
#     for key in new_state:
#         if key != 'socket' and (key not in old_state or not compare_nested_objects(old_state[key], new_state[key])):
#             diff[key] = new_state[key]

#     return json.dumps(diff, indent=2, default=str)

# def copy_context_without_socket(ctx: Ctx) -> Dict:
#     ctx_copy = vars(ctx).copy()
#     ctx_copy.pop('socket', None)
#     return ctx_copy


from typing import Dict, Any
from tangerine import Ctx
import json

def compare_nested_objects(old: Any, new: Any) -> bool:
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

# def generate_diff(old_state: Dict, new_state: Dict) -> str:
#     diff = {}
#     for key in new_state:
#         if key != 'socket' and (key not in old_state or not compare_nested_objects(old_state[key], new_state[key])):
#             diff[key] = new_state[key]

#     return json.dumps(diff, indent=2, default=str)

def generate_diff(old_state: Dict, new_state: Dict) -> str:
    diff = {}

    for key in new_state:
        if key not in old_state or not compare_nested_objects(old_state[key], new_state[key]):
            if key not in old_state:
                diff[key] = {
                    'old': 'none',
                    'new': new_state[key]
                }
            else:
                diff[key] = {
                    'old': old_state[key],
                    'new': new_state[key]
                }

    return json.dumps(diff, indent=2, default=str)
