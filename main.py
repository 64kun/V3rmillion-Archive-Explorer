import json
import argparse
import os


cmd_parser = argparse.ArgumentParser()

cmd_parser.add_argument('path')
cmd_parser.add_argument('-r', required=True, help="threads search", nargs="+")
cmd_parser.add_argument('-pages', type=int, default=1)

cmd_args = cmd_parser.parse_args()

def tonumber(v, default:int=None, Not=False):
    try:
        v = int(v)
        return False if Not else v
    except (ValueError, TypeError):
        return default if not Not else True


FILE_PATH = cmd_args.path
raw_requests = cmd_args.r
REQUESTS = [
    (raw_requests[i], tonumber(raw_requests[i+1] if i+1 < len(raw_requests) else None, default=10))
    for i in range(0, len(raw_requests)) if tonumber(raw_requests[i], Not=True)
]
PAGES = cmd_args.pages

print(REQUESTS)
# threads = os.listdir(FILE_PATH)
# # print(threads[:10])

# found = 0
# for thread in threads:
#     full_path = os.path.join(FILE_PATH, thread)
#     if found != MAX_RESULTS and os.path.exists(os.path.join(full_path, "page_3.html")):
#         found += 1
#         print(full_path)