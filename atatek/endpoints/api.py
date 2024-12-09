import os

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, Response

from atatek.db import get_childs_by_parent, read_tree_by_id, read_tree_info_by_id, add_create_ticket, \
    create_ticket_crud, edit_ticket_crud, create_tree, delete_tree, edit_tree_crud, create_or_update_tree_info, \
    create_new_page, get_all_pages, create_moderator, get_moderator_list_by_page_id, add_popular_person
from atatek.db.crud.users import get_all_user_list, create_or_update_user, get_all_moderator_list
from atatek.utils import get_data, api_token_required, token_required
from atatek.utils.icons import save_file

api = Blueprint('api', __name__)


@api.route('/auth/register/get_place/', methods=['POST'])
def get_place_list():
    country = request.form['country']
    query = request.form['query']
    data = get_data(query, country)
    return data


@api.route('/tree/get/childs/', methods=['POST', 'GET'])
@api_token_required
def get_child():
    data = request.get_json()
    parent_id = data.get('parent_id')
    role = request.role
    childCheck = get_childs_by_parent(parent_id, role)

    response = {
        "status": True,
        "author": "Bagzhan Karl",
        "api": "v3",
        "data": childCheck
    }
    return jsonify(response)

@api.route('/tree/get/childs/token/<int:id>', methods=['GET'])
@api_token_required
def get_child_by_id_for_me(id):
    childCheck = get_childs_by_parent(id, 1)

    response = {
        "status": True,
        "author": "Bagzhan Karl",
        "api": "v3",
        "data": childCheck
    }
    return jsonify(response)


@api.route('/get/<int:id>/info', methods=['POST'])
@api_token_required
def get_info_node(id):
    role = request.role
    item = read_tree_by_id(id)
    item_more = read_tree_info_by_id(id)
    return render_template('modals/info.html', role=role, item=item, item_more=item_more)

@api.route('/ticket/create/add', methods=['POST'])
@token_required
def create_add_ticket():
    childs = request.form.getlist('childname[]')
    role = request.role
    user = request.user_id
    parent = request.form['item']
    ticket = create_ticket_crud('add', user)
    for child in childs:
        add_create_ticket(ticket.id, parent, child)
    return redirect(url_for('main.my_profile_ticket', id=ticket.id))

@api.route('/ticket/create/edit', methods=['POST'])
@token_required
def create_edit_ticket():
    role = request.role
    user = request.user_id

    name = request.form['name']
    birth = request.form.get('birth') or None
    death = request.form.get('death') or None
    biography = request.form['info']
    tree = request.form['item']

    ticket = create_ticket_crud('edit', user)
    data = edit_ticket_crud(
        ticket=ticket.id,
        tree=tree,
        name=name,
        birth=birth,
        death=death,
        biography=biography,
    )
    return redirect(url_for('main.my_profile_ticket', id=ticket.id))

@api.route('/admin/add/', methods=['POST'])
@token_required
def add_child_by_admin():
    parent = request.form['item']
    role = request.role
    if role != 5:
        return 403
    childs = request.form.getlist('childname[]')

    for child in childs:
        create_tree(
            name=child,
            item_id=None,
            parent_id=parent
        )

    return redirect(url_for('main.index'))

@api.route('/admin/delete/<int:id>', methods=['GET'])
@token_required
def admin_delete_child(id):
    ticket = delete_tree(id)
    return redirect(url_for('main.index'))


@api.route('/admin/edit/', methods=['POST'])
@token_required
def edit_child_by_admin():
    user = request.user_id
    item = request.form['item']
    name = request.form['name']
    birth = request.form.get('birth') or None
    death = request.form.get('death') or None

    edit_tree = edit_tree_crud(
        id=item,
        name=name,
        birth=birth,
        death=death,
        updated_by=user
    )
    icon = request.files.get('icon')
    full_icon = request.files.get('full-icon')
    biography = request.form['info'] or None

    upload_folder = 'atatek/static/images/icons/'
    os.makedirs(upload_folder, exist_ok=True)

    saved_icon = save_file(icon, upload_folder) if icon else None
    saved_full_icon = save_file(full_icon, upload_folder) if full_icon else None

    tree_info = create_or_update_tree_info(
        tree=item,
        info=biography,
        updated_by=user,
        created_by=user,
        tree_icon=saved_icon,
        tree_full_icon=saved_full_icon,
    )
    return redirect(url_for('main.index'))

@api.route('/admin/create/newsite', methods=['POST'])
@token_required
def create_new_site():
    item = request.form['item']
    jyz = request.form.get('jyz')
    title = request.form['title']
    breed1 = request.form['breed1']
    breed2 = request.form['breed2']
    breed3 = request.form['breed3']

    page = create_new_page(
        title=title,
        juz=jyz,
        breed1=breed1,
        breed2=breed2,
        breed3=breed3,
        tree=item,
    )
    return redirect(url_for('admin.admin_sites_settings', id=page.id))


@api.route('/admin/users/', methods=['GET'])
@token_required
def get_users():
    users = get_all_user_list()
    data = []
    for user in users:
        data.append({
            'ID': user.id,
            'Имя': user.first_name,
            'Фамилия': user.last_name,
            'Номер телефона': user.phone,
            'Подписка': user.role,
            'Действие': f'<a href="/admin/user/{user.id}">Посмотреть</a>'  # Исправление
        })
    return jsonify({"data": data})


@api.route('/admin/sites/', methods=['GET'])
@token_required
def get_pages():
    pages = get_all_pages()
    data = []
    for page in pages:
        data.append({
            'ID': page.id,
            'Жүз': page.juz,
            'Путь': f'/{page.breed1}/{page.breed2}/{page.breed3}',
            'Название': page.title,
            'Действие': f'<a href="/admin/site/{page.id}">Посмотреть</a>'  # Исправление
        })
    return jsonify({"data": data})

@api.route('/admin/ajax/user/option', methods=['POST'])
@token_required
def get_user_option():
    users = get_all_moderator_list()
    moderators = get_moderator_list_by_page_id(request.form['page'])
    moderator_user_ids = [moderator.user_id for moderator in moderators]
    return render_template('modals/user_options.html', users=users, moderator=moderator_user_ids)

@api.route('/admin/add/moderator', methods=['POST'])
@token_required
def add_moderator():
    moderator = request.form.getlist('moderator')
    page = request.form['page']
    for item in moderator:
        create_moderator(item, page)
    return redirect(url_for('admin.admin_site', id=page))

@api.route('/admin/popular/person', methods=['POST'])
@token_required
def add_popular_person_api():

    fullname = request.form['fullname']
    page = request.form['page']
    birthday = request.form['birthday']
    content = request.form['content']

    upload_folder = 'atatek/static/images/popular/'
    os.makedirs(upload_folder, exist_ok=True)

    image = save_file(request.files['image'], upload_folder)

    person = add_popular_person(
        fullname=fullname,
        birthday=str(birthday),
        content=content,
        page=page,
        image=image,
    )
    return redirect(url_for('admin.admin_site', id=page))

@api.route('/admin/user/change/role/<int:id>', methods=['GET'])
@token_required
def change_user_role(id):
    user = request.user_id
    role = request.role

    newrole = create_or_update_user(
        id=user,
        role=id
    )
    return redirect(url_for('auth.logout'))

@api.route('/FamilyTreeJS', methods=('GET', 'POST'))
def api_tree_data():
    response_content = "<pre>GET: ATATEK FamilyTreeJS</pre>"
    return Response(response_content, content_type="text/html")