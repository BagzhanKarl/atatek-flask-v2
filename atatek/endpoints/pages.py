import json

from flask import Blueprint, request, render_template, redirect, url_for

from atatek.db import get_page_by_breeds, get_parents_list_by_id, get_page_by_id, get_moderator_list_by_page_id, \
    get_all_popular_persons_by_page_id
from atatek.db.crud.news import get_news_all_by_page_id, get_site_settings
from atatek.endpoints.main import settings_path
from atatek.utils import token_required

pages = Blueprint('pages', __name__)

@pages.route('/uly/<string:breed1>/<string:breed2>/<string:breed3>')
@token_required
def show_page_uly(breed1, breed2, breed3):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    role = request.role
    page = get_page_by_breeds(breed1, breed2, breed3)
    if page.juz == 'Ұлы жүз':
        list = get_parents_list_by_id(page.tree_id, lastTouch=True)
        return render_template('main/main.html', page=page, set=settings, start=json.dumps(list))
    else:
        return redirect(url_for('main.index'))

@pages.route('/uly/<string:breed1>/<string:breed2>/<string:breed3>/news')
@token_required
def show_news_page_uly(breed1, breed2, breed3):
    page = get_page_by_breeds(breed1, breed2, breed3)

    news = get_news_all_by_page_id(page.id)
    popular = get_all_popular_persons_by_page_id(page.id)
    site_settings = get_site_settings(page.id)
    return render_template('news/page.html', settings=site_settings, news=news, popular=popular, page=page)


@pages.route('/orta/<string:breed1>/<string:breed2>/<string:breed3>')
@token_required
def show_page_orta(breed1, breed2, breed3):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    role = request.role
    page = get_page_by_breeds(breed1, breed2, breed3)
    if page.juz == 'Орта жүз':
        list = get_parents_list_by_id(page.tree_id, lastTouch=True)
        return render_template('main/main.html', page=page, set=settings, start=json.dumps(list))
    else:
        return redirect(url_for('main.index'))


@pages.route('/kishi/<string:breed1>/<string:breed2>/<string:breed3>')
@token_required
def show_page_kishi(breed1, breed2, breed3):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    role = request.role
    page = get_page_by_breeds(breed1, breed2, breed3)
    if page.juz == 'Кіші жүз':
        list = get_parents_list_by_id(page.tree_id, lastTouch=True)
        return render_template('main/main.html', page=page, set=settings, start=json.dumps(list))
    else:
        return redirect(url_for('main.index'))



@pages.route('/jyztentys/<string:breed1>/<string:breed2>/<string:breed3>')
@token_required
def show_page_jyztentys(breed1, breed2, breed3):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    role = request.role
    page = get_page_by_breeds(breed1, breed2, breed3)
    if page.juz == 'Жүзден тыс':
        list = get_parents_list_by_id(page.tree_id, lastTouch=True)
        return render_template('main/main.html', page=page, set=settings, start=json.dumps(list))
    else:
        return redirect(url_for('main.index'))
