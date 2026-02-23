import json
import argparse
import os
import re
import operator

def tc_parser(v):
    res = re.search(rf"""^tc="?'?([^"']+)"?'?$""", v)
    return res.group(1) if res else None

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
# Supports a `Not` parameter that mirrors the behavior of Python's
# `not` operator. It does not treat 0 as falsy.
def tonumber(v, default:int=None, Not:bool=False):
    try:
        v = int(v)
        return False if Not else v
    except (ValueError, TypeError):
        return default if not Not else True


FILE_PATH = cmd_args.path
print(FILE_PATH)
raw_pages_data = cmd_args.p
PAGES_DATA = {
    "found": 0,
    "min_pages": int(raw_pages_data[0]),
    "max": int(raw_pages_data[1]) if len(raw_pages_data) >= 2 else 10,
    "target_condition": tc_parser(raw_pages_data[2]) or '*' if len(raw_pages_data) == 3 else '*'
}
raw_requests = cmd_args.r
REQUESTS = [
    {raw_requests[i]: {
        "found": 0,
        "max": tonumber(
            raw_requests[i+1] if i+1 < len(raw_requests) else None,
            default=10
        ),
        "threshold": tonumber(
            raw_requests[i+2] if (i+2 < len(raw_requests) and tonumber(
                # safeguard to prevent unintentional utilization of parameters from another request
                raw_requests[i+1],
            )) else None,
            default=1
        ),
        "target_condition": tc_parser(raw_requests[i+3]) or '*' if (
            i+3 < len(raw_requests) and
            tonumber(raw_requests[i+1]) and
            tonumber(raw_requests[i+2])
        ) else '*'
    }}
    for i in range(0, len(raw_requests)) if tonumber(raw_requests[i], Not=True) and not tc_parser(raw_requests[i])
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
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.gt,
}

skip = False
try:
    for thread in threads:
        if skip: break
        # if checked > 1000: break
        checked +=1

        full_path = os.path.join(FILE_PATH, thread)
        thread_data = os.listdir(full_path)
        
        pages = [os.path.join(full_path, f) for f in thread_data if f.endswith('.html')]
        

        if len(pages) < PAGES_DATA["min_pages"]: continue
        
        for data in REQUESTS:
            req, params = next(iter(data.items()))
            if params["target_condition"] == '*':
                pass
            elif params["target_condition"] == '<=' and len(pages) > params["threshold"]:
                continue
            elif params["target_condition"] == '==' and len(pages) != params["threshold"]:
                continue
            # The rest of the code will be here

        
        if not REQUESTS:
            if PAGES_DATA["found"] == PAGES_DATA["max"]: break
            if PAGES_DATA["target_condition"] == '==' and len(pages) != PAGES_DATA["min_pages"]:
                continue
            PAGES_DATA["found"] += 1
            print(full_path)


except KeyboardInterrupt: print("Ctrl + C pressed. Skipped")