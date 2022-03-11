from flask import Blueprint, render_template, request, jsonify, redirect, abort
import utils
import logging

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/main/static')
logging.basicConfig(filename='main.log', level=logging.INFO)


@main.route('/')
def index():
    posts = utils.get_posts_all()
    bookmarks = utils.get_bookmarks()
    if bookmarks is None:
        logging.info('Данные bookmarks не  загружены')
        return 'Данные bookmarks не  загружены'

    if posts is not None:
        return render_template("main/index.html", posts=posts, bookmarks=bookmarks)
    logging.info('Данные постов не загружены')
    return 'Данные постов  не  загружены'


@main.route('/post/<post_id>/', methods=['GET'])
def post_pk(post_id):
    post = utils.get_post_by_pk(int(post_id))
    comments = utils.get_comments_by_post_id(int(post_id))
    if comments is None:
        logging.info(f'Не сформирован список комментариев к посту с ID={post_id}')
        return f'Не сформирован список комментариев к посту с ID={post_id}'

    if post is not None:
        return render_template('main/post.html', post_pk=post, comments=comments)
    logging.info(f'Отсутствуют данные по посту с ID={post_id}')
    return f'Отсутствуют данные по посту с ID={post_id}'


@main.route('/user-feed/<user_name>/', methods=['GET'])
def user_feed(user_name):
    user_posts = utils.get_posts_by_user(user_name)
    if user_posts is not None:
        return render_template('main/user-feed.html', user_posts=user_posts)
    logging.info(f'Отсутствуют данные по пользователю {user_name}')
    return f'Отсутствуют данные по пользователю {user_name}'


@main.route('/tag/<desired_tag>/', methods=['GET'])
def find_tag(desired_tag):
    posts = utils.search_for_posts(desired_tag)
    if posts is not None:
        return render_template('main/tag.html', posts=posts, tag=desired_tag)
    logging.info(f'Отсутствуют данные по тегу {desired_tag}')
    return f'Отсутствуют данные по тегу {desired_tag}'


@main.route('/search', methods=['GET'])
def search_page():
    s = request.args.get("s", "")
    posts = utils.search_for_posts(s)
    if posts is not None:
        return render_template("main/search.html", posts=posts, find_s=s)
    logging.info(f'Поиск по {s} завершился неудачей')
    return f'Поиск по {s} завершился неудачей'


@main.route('/api/posts', methods=['GET'])
def get_all_list_posts():
    posts = utils.get_posts_all()
    return jsonify(posts)


@main.route('/api/posts/<post_id>', methods=['GET'])
def get_post_id(post_id):
    if post_id.isdigit():
        post = utils.get_post_by_pk(int(post_id))
        return jsonify(post)
    logging.info(f'Не верно указан ID поста {post_id}')
    return 'Вернулся  не словарь'


@main.route('/bookmarks/', methods=['GET'])
def get_bookmarks_posts():
    posts_bookmarks = utils.get_bookmarks()
    if posts_bookmarks is not None:
        return render_template("main/bookmarks.html", posts=posts_bookmarks)
    logging.info('Данные постов c bookmarks не  загружены')
    return 'Данные постов c bookmarks не  загружены'


@main.route('/bookmarks/add/<post_id>', methods=['GET'])
def add_bookmarks_post(post_id):
    if post_id.isdigit():
        utils.add_post_bookmarks(int(post_id))
        return redirect("/", code=302)
    logging.info(f'Не верно указан ID поста {post_id}')
    return abort(404)


@main.route('/bookmarks/remove/<post_id>', methods=['GET'])
def remove_bookmarks_post(post_id):
    if post_id.isdigit():
        utils.remove_post_bookmarks(int(post_id))
        return redirect("/", code=302)
    logging.info(f'Не верно указан ID поста {post_id}')
    return abort(404)

