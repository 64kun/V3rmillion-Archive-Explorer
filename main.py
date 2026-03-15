import json
import argparse
import os
import re
import operator
import time
from collections import Counter
from search import search, get_words_list
from thread_parser import thread_parser

# def tc_parser(v):
#     res = re.search(r"""^tc="?'?(\W+)(\d+)"?'?$""", v)
#     return (res.group(1), int(res.group(2))) if res else None


# def p_flag_type(v):
#     try:
#         return int(v)        
#     except ValueError:
#         if not tc_parser(v):
#             raise argparse.ArgumentTypeError(f"invalid int value or value is not tc parameter: '{v}'")
#         return v


cmd_parser = argparse.ArgumentParser()

cmd_parser.add_argument('path', help="path to v3rmillion folder")
cmd_parser.add_argument('-r', help="threads search", default=[], nargs='*')
cmd_parser.add_argument('-d', action='store_true', help='debug')
# cmd_parser.add_argument(
#     '-p', type=p_flag_type, required=True, nargs="+",
#     help="""minimum pages for all threads (global). uses 2nd arg or a default value as max results if -r are empty.
#     also have `tc` parameter, that uses only if -r are empty"""
# )
# cmd_parser.add_argument('-priority', choices=['request', 'pages', 'pages-proximity'], default='request')
# cmd_parser.add_argument('--ascending-sort', action="store_true")

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
DEBUG = cmd_args.d
# print(FILE_PATH)
# raw_pages_data = cmd_args.p
# PAGES_DATA = {
#     "found": 0,
#     "min_pages": raw_pages_data[0],
#     "max_results": raw_pages_data[1] if len(raw_pages_data) >= 2 else 10,
#     "target_condition": (tc_parser(raw_pages_data[2]) or (None, 1)) if len(raw_pages_data) == 3 else (None, 1)
# }
# print(PAGES_DATA)
raw_requests = cmd_args.r
REQUESTS = [
    {raw_requests[i].lower(): {
        # "found": [],
        "max_results": tonumber(
            raw_requests[i+1] if i+1 < len(raw_requests) else None,
            default=10
        ),
        # "target_condition": tc_parser(raw_requests[i+2]) or (None, 1) if (
        #     i+2 < len(raw_requests) and
        #     tonumber(raw_requests[i+1], Is=True)
        # ) else (None, 1)
    }}
    for i in range(0, len(raw_requests)) if tonumber(raw_requests[i], not_is=True) #and not tc_parser(raw_requests[i])
]

# print(REQUESTS)
# threads = os.listdir(FILE_PATH)

# OPS = {
#     '==': operator.eq,
#     '!=': operator.ne,
#     '<=': operator.le,
#     '>=': operator.ge,
#     '<': operator.lt,
#     '>': operator.gt,
# }

# def default_OPS_predicate(a, b):
#     return True

WORDS_RE = re.compile(r"\w+")

def get_words_list(s):
    return WORDS_RE.findall(s) if s else []


# all_max_results = 0

# for data in REQUESTS:
#     _, params = next(iter(data.items()))
#     all_max_results += params["max_results"]

# if not REQUESTS:
#     all_max_results += PAGES_DATA["max_results"]

# print("all results should found:", all_max_results)


def main():
    for data in REQUESTS:
        req, params = next(iter(data.items()))
        if not req:
            continue

        max_results = params['max_results']

        result_ids = search(req, max_results)
        if not result_ids:
            continue
        
        threads = [thread_parser(os.path.join(FILE_PATH, r), debug=DEBUG) for r in result_ids]

        req_folder = os.path.join('parsed', '-'.join(get_words_list(req)))

        if not os.path.exists(req_folder):
            os.makedirs(req_folder, exist_ok=True)
        
        for i, (id, thread) in enumerate(zip(result_ids, threads), start=1):
            path_to_save = os.path.join(req_folder, f'{i}_parsed-thread_{id}.json')

            with open(path_to_save, 'w', encoding='utf-8') as f:
                json.dump(thread, f, ensure_ascii=False, indent=4)

            print(f'Saved thread {id} to {path_to_save}')


main()


# last_iterate = 0
# last_thread = None

# def main():
#     global last_iterate, last_thread
#     for thread in threads[last_iterate:]:
#         last_iterate += 1
#         last_thread = thread
#         full_path = os.path.join(FILE_PATH, thread)
#         thread_data = os.listdir(full_path)
#         # print("\rChecking", last_iterate, end='')
        
#         pages = [os.path.join(full_path, f) for f in thread_data if f.endswith('.html')]
#         pages_len = len(pages)

#         if pages_len < PAGES_DATA["min_pages"]: continue
        
#         current_total_found = 0
#         with open(os.path.join(full_path, "thread.json"), 'r', encoding='utf-8') as f:
#             thread_title = json.load(f)["title"].lower()

#             for data in REQUESTS:
#                 req, params = next(iter(data.items()))
#                 threads_found = len(params["found"])
#                 current_total_found += threads_found

#                 if threads_found == params["max_results"]:
#                     continue

#                 target_condition, threshold = params["target_condition"]
#                 if not OPS.get(target_condition, default_OPS_predicate)(pages_len, threshold):
#                     continue

#                 if parser(req, thread_title):
#                     params["found"].append(full_path)
#                     current_total_found += 1
#                     print("По запросу", req, "найдено", full_path)

                
#             # The rest of the code will be here

#         if not REQUESTS:
#             current_total_found += PAGES_DATA["found"]

#             target_condition, threshold = PAGES_DATA["target_condition"]
#             if not OPS.get(target_condition, default_OPS_predicate)(pages_len, threshold):
#                 continue

#             PAGES_DATA["found"] += 1
#             current_total_found += 1
#             print(full_path)

#         if current_total_found == all_max_results:
#             return True


# while True:
#     try:
#         if main():
#             break
#     except KeyboardInterrupt:
#         print("Ctrl + C pressed. The last thread the loop was running on:", last_thread + '.',
#               "Also, the last iterate is", last_iterate)
#         if input("Continue? (y/n) ").lower() in 'n':
#             break
