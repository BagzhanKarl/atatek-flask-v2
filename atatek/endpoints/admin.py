import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from atatek.db import get_page_by_id, get_moderator_list_by_page_id, delete_moderator, \
    get_all_popular_persons_by_page_id
from atatek.db.crud.news import create_news_admin, get_news_all_by_page_id
from atatek.db.crud.users import get_user_by_id
from atatek.utils import token_required
from atatek.utils.icons import save_file

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@token_required
def admin_index():
    return render_template('admin/users.html')

@admin.route('/sites')
@token_required
def admin_sites():
    return render_template('admin/sites.html')

@admin.route('/site/<int:id>')
@token_required
def admin_site(id):
    page = get_page_by_id(id)
    asdf = get_moderator_list_by_page_id(page.id)
    moderators = []
    news = get_news_all_by_page_id(page.id)
    popular = get_all_popular_persons_by_page_id(page.id)
    for moderator in asdf:
        user = get_user_by_id(moderator.user_id)
        moderators.append({
            "id": user.id,
            "mod": moderator.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": moderator.created_at,
        })
    return render_template('admin/site.html', page=page, moderators=moderators, news=news, popular=popular)


@admin.route('/site/<int:id>/save_news', methods=['POST'])
@token_required
def admin_site_news_new(id):
    try:
        # Проверяем наличие необходимых данных
        if 'title' not in request.form:
            return jsonify({'error': 'Название новости обязательно'}), 400
        if 'content' not in request.form:
            return jsonify({'error': 'Контент новости обязателен'}), 400
        if 'poster' not in request.files:
            return jsonify({'error': 'Постер новости обязателен'}), 400

        upload_folder = 'atatek/static/images/news/'
        os.makedirs(upload_folder, exist_ok=True)

        # Сохраняем файл и получаем новое имя
        poster_filename = save_file(request.files['poster'], upload_folder)

        news = create_news_admin(id,content=request.form['content'], title=request.form['title'], poster=poster_filename)

        return jsonify({
            'success': True,
            'message': 'Новость успешно сохранена',
            'news_id': news.id
        })

    except Exception as e:

        return jsonify({
            'error': f'Произошла ошибка при сохранении новости: {str(e)}'
        }), 500

@admin.route('/user/<int:id>')
@token_required
def admin_user(id):
    return render_template('admin/site.html')

@admin.route('/tickets')
@token_required
def admin_tickets():
    return render_template('admin/tickets.html')

@admin.route('/ticket/<int:id>')
@token_required
def admin_ticket(id):
    pass

@admin.route('/roles')
@token_required
def admin_roles():
    return render_template('admin/roles.html')


@admin.route('/role/<int:id>')
@token_required
def admin_role(id):
    pass

@admin.route('/moderator/delete/<int:id>/<int:page>')
@token_required
def admin_moderator_delete(id, page):
    delete = delete_moderator(id)
    return redirect(url_for('admin.admin_site', id=page))