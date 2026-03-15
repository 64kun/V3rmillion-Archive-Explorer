import re, os, json
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import TypedDict, List

LIKE_BUTTONS_RE = re.compile(r'^like_buttons\d+$')
REPLIED_TO_RE = re.compile(r'^\s*(.*)\s+Wrote')
POST_DESCRIPTION_RE = re.compile(r'^\s+|\s+$') 
REPLIED_TO_MESSAGE_DATE_RE = re.compile(r'\b[^\)]+')

PAGE_RE = re.compile(r'\d+')

FULL_WORDS_RE = re.compile(r"\S+")

def get_words_list(s):
    return FULL_WORDS_RE.findall(s) if s else []


# get only element text
def get_only_el_text(element: Tag, strip=False) -> str:
    return element and ''.join([c.get_text(strip=strip) for c in element.contents if isinstance(c, NavigableString)]) or ''


def get_text_start(text, p=0.08):
    if not text: return None
    # text_words = get_words_list(text)
    # words_count_pattern = round((len(text_words) * p) + 1) * r"\s*\S+"
    # return re.search(words_count_pattern, text).group()
    return text[:round(len(text) * p + 1)]

def get_post_information(post: Tag, page_content: Tag, debug=False, page=None, i=None):
    if debug:
        print(f"Parsing {i+1} post in {page} page.\nPost:\n{post}")

    post_date_element = post.select_one(".post_date")
    post_date = get_only_el_text(post_date_element, strip=True)

    last_edit_element = post.select_one('.post_date .edited_post')
    last_edit = last_edit_element and last_edit_element.get_text(strip=True, separator=' ') or None

    post_content_element = post.select_one('.post_content')
    
    like_buttons_element = (
        post_content_element.find(attrs={'id': LIKE_BUTTONS_RE}) or
        post.find(attrs={'id': LIKE_BUTTONS_RE}) or
        page_content.find_all(attrs={'id': LIKE_BUTTONS_RE})[i]
    )

    likes = like_buttons_element.select_one('.fa.fa-thumbs-o-up').parent.parent.get_text(strip=True)
    dislikes = like_buttons_element.select_one('.fa.fa-thumbs-o-down').parent.parent.get_text(strip=True)

    post_body_element = post_content_element.select_one('.post_body.scaleimages')
    links = post_body_element.select('a[href]')
    images = post_body_element.select('img[src]')
    
    for link_element in links:
        link_element.replace_with(link_element.get('href'))

    for image_element in images:
        image_element.replace_with(image_element.get('src'))

    author_username = post_body_element.get('data-username')
    author_id = post_body_element.get('id')
    
    blockquote_elements = post_body_element.select('blockquote')
    blockquote_element = None
    for quote in blockquote_elements:
        cite_text = get_only_el_text(quote.find('cite'))
        if 'quote:' in cite_text.lower():
            continue
        elif REPLIED_TO_RE.search(cite_text):
            blockquote_element = quote
            break

    blockquote_element_text = None

    replied_to_message_date = None
    replied_to = None
    replied_post_start = None

    post_description = None

    if blockquote_element:
        blockquote_element_text = POST_DESCRIPTION_RE.sub('', blockquote_element.get_text())
        
        cite_element = blockquote_element.find('cite')

        replied_to = REPLIED_TO_RE.search(get_only_el_text(cite_element, strip=True)).group(1)
        
        replied_to_message_date = REPLIED_TO_MESSAGE_DATE_RE.search(cite_element.find('span').get_text(strip=True)).group()
        
        replied_post_text = POST_DESCRIPTION_RE.sub('', get_only_el_text(blockquote_element))
        replied_post_start = get_text_start(replied_post_text)

        blockquote_element.decompose()
    
    post_description = POST_DESCRIPTION_RE.sub('', post_body_element.get_text())

    post_description_start = get_text_start(post_description)

    # print(post_description)

    return (blockquote_element_text, {                       # comments bellow are the templates
        'post_date': post_date,                              # '05-01-2023, 02:18 AM'
        'last_edit': last_edit,                              # '(This post was last modified: 04-30-2023, 10:46 PM by USERNAME .)'
        'likes': likes,                                      # '10'
        'dislikes': dislikes,                                # '2'
        'author_username': author_username,                  # 'USERNAME'
        'author_id': author_id,                              # 'pid_xxxxxxx'
        'replied_to': replied_to,                            # 'USERNAME'
        'replied_to_post_date': replied_to_message_date,     # '04-28-2023, 05:53 PM'
        'post_description': post_description,                # str
        'post_description_start': post_description_start,    # first 5% of post_description (my super idea)
        'replied_post_start': replied_post_start,            # first 5% of replied post
        'replies': []
    })


def sortpages(v):
    return int(PAGE_RE.search(v).group())


class Post(TypedDict):
    post_date: str
    last_edit: str
    likes: str
    dislikes: str
    author_username: str
    author_id: str
    replied_to: str
    replied_to_post_date: str
    post_description: str
    post_description_start: str
    replied_post_start: str
    replies: List['Post']


class Thread(TypedDict):
    thread_path: str
    title: str
    thread_content: Post
    replies_to_not_found_posts: List[Post]


def thread_parser(folder_path, debug=False, save_after_parse=False, path_to_save='') -> Thread:
    print(f"Parsing thread {folder_path}...")
    pages = sorted([f for f in os.listdir(folder_path) if f.endswith('.html')], key=sortpages)

    thread_tree = {'thread_path': folder_path, 'title': None,
                   'thread_content': None, 'replies_to_not_found_posts': []}
    posts_pos = dict()
    
    got_thread_content_info = False

    for page in pages:
        with open(os.path.join(folder_path, page), "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        posts = soup.select('.post')

        if not got_thread_content_info:
            title_tag = soup.select_one('head title')
            title = title_tag and title_tag.text or None
            thread_tree['title'] = title
            # print(title)

            _, thread_content_info = get_post_information(posts[0], soup, debug=debug, page=page, i=0)
            
            post_date, author_username, post_description_start = thread_content_info['post_date'], thread_content_info['author_username'], thread_content_info['post_description_start']
            posts_pos[(post_date, author_username)] = thread_content_info
            posts_pos[(post_date, post_description_start)] = thread_content_info

            thread_tree['thread_content'] = thread_content_info


        for i in range(int(not got_thread_content_info), len(posts)):
            blockquote_element_text, post_info =  get_post_information(posts[i], soup, debug=debug, page=page, i=i)
            
            post_date, author_username, post_description_start = post_info['post_date'], post_info['author_username'], post_info['post_description_start']
            posts_pos[(post_date, author_username)] = post_info
            posts_pos[(post_date, post_description_start)] = post_info

            replied_to_message_date, replied_to, replied_post_start = post_info["replied_to_post_date"], post_info['replied_to'], post_info['replied_post_start']
            if replied_to_message_date and replied_to:
                replied_post = posts_pos.get((replied_to_message_date, replied_to)) or posts_pos.get((replied_to_message_date, replied_post_start))
                if replied_post:
                    # print('found!')
                    replied_post['replies'].append(post_info)
                else:
                    # print('erm..')
                    thread_tree['replies_to_not_found_posts'].append(post_info)
                    post_info['quote'] = blockquote_element_text
            else:
                # print('found!!')
                thread_tree['thread_content']['replies'].append(post_info)
        
        # print(list(posts_pos.keys()))
        got_thread_content_info = True
    
    if save_after_parse:
        if not path_to_save:
            _, thread_id = os.path.split(folder_path)
            path_to_save = os.path.join('parsed', f'parsed_thread_{thread_id}')

        with open(path_to_save, 'w', encoding='utf-8') as f:
            json.dump(thread_tree, f, ensure_ascii=False, indent=4)

        print(f"Parsed thread saved to {path_to_save}")

    return thread_tree
