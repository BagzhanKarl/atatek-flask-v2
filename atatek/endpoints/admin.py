import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from atatek.db import get_page_by_id, get_moderator_list_by_page_id, delete_moderator, \
    get_all_popular_persons_by_page_id, get_all_roles, get_role_by_id, update_role, get_place_by_osm
from atatek.db.crud.news import create_news_admin, get_news_all_by_page_id, create_site_settings
from atatek.db.crud.users import get_user_by_id, create_subscription, get_active_subs_by_id
from atatek.utils import token_required
from atatek.utils.icons import save_file

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@token_required
def admin_index():
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    return render_template('admin/users.html')

@admin.route('/sites')
@token_required
def admin_sites():
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    return render_template('admin/sites.html')

@admin.route('/site/<int:id>/settings/', methods=['GET', 'POST'])
@token_required
def admin_sites_settings(id):
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        upload_folder = 'atatek/static/images/news/sites'
        os.makedirs(upload_folder, exist_ok=True)

        logo = save_file(request.files['logosite'], upload_folder)
        poster = save_file(request.files['postersite'], upload_folder)
        description = request.form['description']

        create_site_settings(
            page=id,
            logo=logo,
            newsletter_bg=poster,
            icon=logo,
            description=description,
        )
        return redirect(url_for('admin.admin_site', id=id))

    page = get_page_by_id(id)

    return render_template('admin/site-settings.html', page=page)

@admin.route('/site/<int:id>')
@token_required
def admin_site(id):
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
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
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
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
    user = get_user_by_id(id)
    address = get_place_by_osm(user.address)
    UserRole = get_role_by_id(user.role)
    roles = get_all_roles()
    subs = get_active_subs_by_id(user.id)
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    return render_template('admin/user.html', user=user, roles=roles, address=address, role=UserRole, subs=subs)

@admin.route('/tickets')
@token_required
def admin_tickets():
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    return render_template('admin/tickets.html')

@admin.route('/ticket/<int:id>')
@token_required
def admin_ticket(id):
    role = request.role
    if role != 5:
        return redirect(url_for('main.index'))
    pass

@admin.route('/roles')
@token_required
def admin_roles():
    role = request.role
    roles = get_all_roles()

    if role != 5:
        return redirect(url_for('main.index'))
    return render_template('admin/roles.html', roles=roles)


@admin.route('/role/<int:id>', methods=['GET', 'POST'])
@token_required
def admin_role(id):
    if request.method == 'POST':
        title = request.form['title']
        add_child = request.form['add_child']
        add_info = request.form['add_info']
        personal_page = True if request.form.get('personal_page') else False
        all_pages = True if request.form.get('all_pages') else False
        price = request.form['price']

        update_role(
            role_id=id,
            title=title,
            add_child=add_child,
            add_info=add_info,
            price=price,
            personal=personal_page,
            all_pages=all_pages,
        )

        return redirect(url_for('admin.admin_roles'))
    else:
        role = request.role
        roles = get_role_by_id(id)
        if role != 5:
            return redirect(url_for('main.index'))
        return render_template('admin/role.html', role=roles)

@admin.route('/moderator/delete/<int:id>/<int:page>')
@token_required
def admin_moderator_delete(id, page):
    delete = delete_moderator(id)
    return redirect(url_for('admin.admin_site', id=page))


@admin.route('/user/change/role', methods=['POST'])
def admin_user_change():
    user = request.form['user_id']
    role = request.form['role']
    create_subscription(user, role)
    return redirect(url_for('admin.admin_user', id=user))