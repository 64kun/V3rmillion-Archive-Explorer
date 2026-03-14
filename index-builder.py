# This script was used for the index.json build

import os, re, json
from collections import defaultdict

# use this variable for building
ARCHIVE_PATH = r"C:\Absolute_Everything\v3rmillion-archive\v3rmillion\threads"
threads = os.listdir(ARCHIVE_PATH)

WORDS_RE = re.compile(r"\w+") # not \S+ because yes
def get_words_list(s):
    return WORDS_RE.findall(s) if s else []

index = defaultdict(list)

def main():
    for i, thread in enumerate(threads):
        if i % 1000 == 0:
            print("\rParsed and added", i, "threads.", end='')

        full_path = os.path.join(ARCHIVE_PATH, thread)
        try:
            with open(os.path.join(full_path, "thread.json"), 'r', encoding='utf-8') as f:
                thread_title_words = get_words_list(json.load(f)["title"].lower())
                for w in set(thread_title_words):
                    index[w].append(thread)
        except Exception as e:
            print(f"Skipped {thread}: {e}") # only 1 thread been skipped in process, lol


main()

with open("index/index.json", "w", encoding="utf-8") as f:
    json.dump(dict(index), f, ensure_ascii=False, indent=2)


print("\nIndex built. Words:", len(index))