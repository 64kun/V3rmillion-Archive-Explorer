import re, json, os
from thread_parser import thread_parser
from math import log

WORDS_RE = re.compile(r"\w+")
# FILE_PATH = r"C:\Absolute_Everything\v3rmillion-archive\v3rmillion\threads"

def get_words_list(s):
    return WORDS_RE.findall(s) if s else []

with open('index/index.json', 'r', encoding='utf-8') as f:
    index: dict = json.load(f)

def search(req, max_results, path):
    req_words = get_words_list(req)
    scores = {}

    # time: O(len(req_words) * len(candidate))
    for word in req_words:
        candidate = index.get(word)
        if not candidate:
            continue
        
        for thread_id in candidate:
            scores[thread_id] = scores.get(thread_id, 0) + log(1028899 / len(candidate))

    results = sorted(scores, key=scores.get, reverse=True)
    results = len(results) >= max_results and results[:max_results] or results
    
    return (results, [thread_parser(os.path.join(path, r)) for r in results])

    


# # def post_generator(post):
                     
# for i, r in enumerate(results):
#     thread_path = os.path.join(FILE_PATH, r)
#     print("Thread found! See:", thread_path)

#     parsed_thread = thread_parser(thread_path)
#     # title = parsed_thread["title"]
#     # thread_content = parsed_thread["thread_content"]

#     # title_word = 'Thread title: '
#     # author_word = "Thread Author: "
#     # description_word = "Thread description:"
#     # i'll make later beautiful format or MAYBE another html
#     # thread = f'{' ' * (round(len(title) / 2) - round(len(title_word) / 2 + 0.5))}{title_word}\n{'-' * len(title)}\n{title}\n{'-' * len(title)}\n'
    
#     # thread = title_word + title + '\n'
#     # thread += author_word + thread_content["author_username"] + '\n\n'
#     # thread += description_word + '\n' + thread_content['post_description'] + '\n'
#     # thread_content
#     # print(thread)

#     with open(f'parsed/{i}_parsed_thread_{r}.json', 'w', encoding='utf-8') as f:
#         json.dump(parsed_thread, f, ensure_ascii=False, indent=4)
#         print(f'parsed thread {r} saved in json to parsed/{i}_parsed_thread_{r}.json')

#     # with open(f'thread_{r}.txt', 'w', encoding='utf-8') as f:
#     #     f.write(thread)


# print("Done!")

