import argparse
from thread_parser import thread_parser

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument('path', nargs='*', default=[])
cmd_args = cmd_parser.parse_args()

THREADS_PATH = cmd_args.path

for path in THREADS_PATH:
    thread_parser(path, save_after_parse=True)