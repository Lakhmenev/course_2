import json
import os
from json import JSONDecodeError
import logging
# from pprint import pprint as pp

logging.basicConfig(filename='utils.log', level=logging.INFO)

DATA_PATH = './data/data.json'
COMMENTS_PATH = './data/comments.json'
BOOKMARKS_PATH = './data/bookmarks.json'


def load_data_from_json(name_file):
    """
    Функция загрузки данных из файла json
    :param name_file: имя файла
    :return: данные из файла
    """
    if os.path.isfile(name_file):
        with open(name_file, 'r', encoding='utf8') as json_file:
            try:
                data_json = json.load(json_file)
            except JSONDecodeError:
                logging.info(f'Ошибка обработки data.json файла!')
                return None
            else:
                return data_json
    else:
        return None


def get_posts_all():
    """
    Функция  возвращает список всех постов
    :return: список
    """
    posts = load_data_from_json(DATA_PATH)
    if posts is not None:
        return posts
    return None


def get_bookmarks():
    """
    Функция  возвращает список постов с закладками
    :return: список
    """
    posts = load_data_from_json(DATA_PATH)
    bookmarks = load_data_from_json(BOOKMARKS_PATH)
    posts_bookmarks = []
    if bookmarks is not None:
        for post in posts:
            for bookmark in bookmarks:
                if post['pk'] == bookmark['pk']:
                    posts_bookmarks.append(post)
        return posts_bookmarks
    return None


def get_posts_by_user(user_name: str):
    """
    Функция получения постов определенного пользователя
    :param user_name: имя пользователя
    :return: список постов пользователя
    """
    posts = load_data_from_json(DATA_PATH)
    if posts is not None:
        user_posts = []
        for post in posts:
            if user_name.lower() == post['poster_name'].lower():
                user_posts.append(post)
        user_posts = add_list_hashtag(user_posts)
        return user_posts
    else:
        return None


def get_comments_by_post_id(post_id: int):
    """
    Функция получения комментарии к посту
    :param post_id: идентификатор поста
    :return: список  комментариев
    """
    comments = load_data_from_json(COMMENTS_PATH)
    if comments is not None:
        comments_post = []
        for comment in comments:
            if post_id == comment['post_id']:
                comments_post.append(comment)
        return comments_post
    return None


def search_for_posts(query: str):
    """
    Функция получает список постов по вхождению
    хештега или строки в описание поста
    :param query: искомая подстрока
    :return: список найденных постов плюс в словарь добавлен
             новый ключь 'hashtag' со списком хештегов в описание к посту
    """
    posts = load_data_from_json(DATA_PATH)
    if posts is not None:
        search_posts = []
        for post in posts:
            if query.lower() in post['content'].lower():
                search_posts.append(post)
        search_posts = add_list_hashtag(search_posts)
        return search_posts
    return None


def get_post_by_pk(pk: int):
    """
    Функция получает пост по его идентификатору
    :param pk: идентификатор
    :return: словарь с данными  поста
    """
    posts = load_data_from_json(DATA_PATH)
    if posts is not None:
        temp_post = None
        for post in posts:
            if pk == post['pk']:
                temp_post = post
                break
        return temp_post
    return None


def add_list_hashtag(posts):
    """
    Функция формирует список хештегов по ключу 'content'
    и добавляет его в словарь с ключём 'hashtag'
    :param posts: список  словарей
    :return: список словарей  с новым ключём 'hashtag', содержащим список найденных хештегов
    """
    hashtag_list = []
    tag = ''
    fl_tag = False
    for post in posts:
        for litter in post['content']:
            if litter == '#':
                fl_tag = True
                tag += litter
            elif fl_tag and litter.isalpha():
                tag += litter
            else:
                if fl_tag and len(tag) > 1:
                    hashtag_list.append(tag)
                tag = ''
                fl_tag = False
        post['hashtag'] = hashtag_list
        hashtag_list = []
    return posts


def add_post_bookmarks(post_id: int):
    """
    Функция добавления идентификатора поста в закладки
    :param post_id: идентификатор поста
    :return: None
    """
    list_bookmarks = load_data_from_json(BOOKMARKS_PATH)
    flag_presence = False

    # Проверка если уже пост в закладках
    for bookmark in list_bookmarks:
        if post_id in bookmark.values():
            flag_presence = True

    # Если поста нет то добавляем в закладки
    if not flag_presence:
        bookmark = {'pk': post_id}
        list_bookmarks.append(bookmark)
        logging.info(f'Пост "pk":{post_id} добавлен в закладки!')
        record_bookmarks(list_bookmarks)
        return


def remove_post_bookmarks(post_id: int):
    """
    Функция удаления поста из закладок
    :param post_id: идентификатор поста
    :return: None
    """
    list_bookmarks = load_data_from_json(BOOKMARKS_PATH)
    bookmark = {'pk': post_id}
    try:
        list_bookmarks.remove(bookmark)
    except ValueError:
        logging.info(f'Ошибка удаления поста "pk":{post_id} ')
    else:
        logging.info(f'Пост "pk":{post_id} удален!')
        record_bookmarks(list_bookmarks)
    return


def record_bookmarks(record_list):
    """
    Функция  записи результатов изменения в закладках
    :param record_list: список для  записи в файл
    :return: None
    """
    try:
        with open(BOOKMARKS_PATH, 'w', encoding='utf8') as json_file:
            json.dump(record_list, json_file, ensure_ascii=False)
            logging.info(f'Файл закладок обновлён!')
    except FileNotFoundError:
        logging.info(f'Файл закладок не найден!')
    except JSONDecodeError:
        logging.info(f'Ошибка обработки bookmarks.json файла!')


# pp(get_posts_all())
# pp(get_posts_by_user('leo'))
# pp(get_comments_by_post_id(1))
# pp(search_for_posts('катер'))
# pp(get_post_by_pk(2))
# pp(get_bookmarks())
# pp(add_post_bookmarks(2))
# pp(remove_post_bookmarks(55))
