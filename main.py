import json
import argparse
import os


cmd_parser = argparse.ArgumentParser()

cmd_parser.add_argument('path', help="path to v3rmillion folder")
cmd_parser.add_argument('-r', help="threads search", nargs="+")

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
raw_requests = cmd_args.r
REQUESTS = [
    {raw_requests[i]: {
        0: tonumber(
            raw_requests[i+1] if i+1 < len(raw_requests) else None,
            default=10
        ),
        "pages": tonumber(
            raw_requests[i+2] if (i+2 < len(raw_requests) and tonumber(
                # safeguard to prevent unintentional utilization of parameters from another request
                raw_requests[i+1] ,
            )) else None,
            default=1
        ),
    }}
    for i in range(0, len(raw_requests)) if tonumber(raw_requests[i], Not=True)
]

print(REQUESTS)
# threads = os.listdir(FILE_PATH)
# # print(threads[:10])

# for thread in threads:
#     full_path = os.path.join(FILE_PATH, thread)

#     if found != MAX_RESULTS and 
#         found += 1
#         print(full_path)