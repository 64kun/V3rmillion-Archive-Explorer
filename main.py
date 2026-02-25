import json
import argparse
import os
import re
import operator
import time

def tc_parser(v):
    res = re.search(r"""^tc="?'?(\W+)(\d+)"?'?$""", v)
    return (res.group(1), int(res.group(2))) if res else None


def p_flag_type(v):
    try:
        return int(v)        
    except ValueError:
        if not tc_parser(v):
            raise argparse.ArgumentTypeError(f"invalid int value or value is not tc parameter: '{v}'")
        return v


cmd_parser = argparse.ArgumentParser()

cmd_parser.add_argument('path', help="path to v3rmillion folder")
cmd_parser.add_argument('-r', help="threads search", default=[], nargs='*')
cmd_parser.add_argument(
    '-p', type=p_flag_type, required=True, nargs="+",
    help="""minimum pages for all threads (global). uses 2nd arg or a default value as max results if -r are empty.
    also have `tc` parameter, that uses only if -r are empty"""
)
cmd_parser.add_argument('-priority', choices=['request', 'pages', 'pages-proximity'], default='request')
cmd_parser.add_argument('--ascending-sort', action="store_true")

cmd_args = cmd_parser.parse_args()

# Imitates the C function `tonumber` from Lua.
# Supports a `not_is` and `Is` parameters that mirrors the behavior of Python's
# `not` & `and` operators. It does not treat 0 as falsy.
def tonumber(v, default:int=None, not_is:bool=False, Is:bool=False):
    try:
        v = int(v)
        return False if not_is else (v if not Is else True)
    except (ValueError, TypeError):
        return (default if not Is else False) if not not_is else True


FILE_PATH = cmd_args.path
print(FILE_PATH)
raw_pages_data = cmd_args.p
PAGES_DATA = {
    "found": 0,
    "min_pages": raw_pages_data[0],
    "max_results": raw_pages_data[1] if len(raw_pages_data) >= 2 else 10,
    "target_condition": tc_parser(raw_pages_data[2]) if len(raw_pages_data) == 3 else None
}
print(PAGES_DATA)
raw_requests = cmd_args.r
REQUESTS = [
    {raw_requests[i]: {
        "found": 0,
        "max_results": tonumber(
            raw_requests[i+1] if i+1 < len(raw_requests) else None,
            default=10
        ),
        "target_condition": tc_parser(raw_requests[i+2]) or (None, 1) if (
            i+2 < len(raw_requests) and
            tonumber(raw_requests[i+1], Is=True)
        ) else (None, 1)
    }}
    for i in range(0, len(raw_requests)) if tonumber(raw_requests[i], not_is=True) and not tc_parser(raw_requests[i])
]

print(REQUESTS)
threads = os.listdir(FILE_PATH)
# print(threads[:10])

def parser(r, title):
    return


checked = 0
g = []

OPS = {
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.gt,
}

def default_OPS_predicate(a, b):
    return True


skip = False
try:
    for thread in threads:
        if skip: break
        # if checked > 1000: break
        checked +=1

        full_path = os.path.join(FILE_PATH, thread)
        thread_data = os.listdir(full_path)
        
        pages = [os.path.join(full_path, f) for f in thread_data if f.endswith('.html')]
        pages_len = len(pages)

        if pages_len < PAGES_DATA["min_pages"]: continue
        
        for data in REQUESTS:
            req, params = next(iter(data.items()))
            target_condition, threshold = params["target_condition"]
            if not OPS.get(target_condition, default_OPS_predicate)(pages_len, threshold):
                continue
            time.sleep(0.01)
            print("found")
            # The rest of the code will be here
        
        if not REQUESTS:
            if PAGES_DATA["found"] == PAGES_DATA["max_results"]: break
            target_condition, threshold = PAGES_DATA["target_condition"]
            if not OPS.get(target_condition, default_OPS_predicate)(pages_len, threshold):
                continue
            PAGES_DATA["found"] += 1
            print(full_path)


except KeyboardInterrupt: print("Ctrl + C pressed. Skipped")