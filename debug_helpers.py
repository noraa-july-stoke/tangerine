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
