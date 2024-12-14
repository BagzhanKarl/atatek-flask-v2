import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response

from atatek.db import User, get_place_by_osm, get_parents_list_by_id, get_page_by_id, get_user_tickets_all, \
    get_user_ticket_by_id, get_all_roles, get_role_by_id
from atatek.db.crud.family import check_user_family, create_record_for_table, update_record_for_table, get_my_tree, \
    create_record_by_ui, update_record_by_ui, get_tree_count, remove_node_by_id
from atatek.db.crud.users import get_user_by_id, get_active_subs_by_id, create_or_update_user, update_login_token
from atatek.utils import token_required

main = Blueprint('main', __name__)
settings_path = os.path.join(os.path.dirname(__file__), '../utils/settings.json')
family_path = os.path.join(os.path.dirname(__file__), '../utils/package.json')

@main.route('/')
@token_required
def index():
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    page = request.page
    role = request.role
    startList = []
    startList.append({
        "id": 1,
        "name": 'Алаш',
        "born": None,
        "death": None,
        "info": True,
        "role": role,
        "untouchable": False,
    })

    return render_template('main/main.html', page=get_page_by_id(page), set=settings, start=json.dumps(startList))

@main.route('/my/')
@token_required
def my_page():
    role = request.role
    page = request.page
    if role > 1 and role < 6:
        page_link = get_page_by_id(page)
        if page_link.juz == 'Ұлы жүз':
            link = f'https://uly-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}'
        elif page_link.juz == 'Орта жүз':
            link = f'https://orta-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}'
        elif page_link.juz == 'Кіші жүз':
            link = f'https://kishi-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}'
        elif page_link.juz == 'Жүзден тыс':
            link = f'https://jyzden-tys.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}'
        return redirect(link)
    else:
        return redirect('/no-access/tariff-plans')

@main.route('/my/news')
@token_required
def my_news():
    role = request.role
    page = request.page
    if role > 1 and role < 6:
        page_link = get_page_by_id(page)
        if page_link.juz == 'Ұлы жүз':
            link = f'https://uly-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}/news'
        elif page_link.juz == 'Орта жүз':
            link = f'https://orta-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}/news'
        elif page_link.juz == 'Кіші жүз':
            link = f'https://kishi-jyz.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}/news'
        elif page_link.juz == 'Жүзден тыс':
            link = f'https://jyzden-tys.atatek.kz/{page_link.breed1}/{page_link.breed2}/{page_link.breed3}/news'
        return redirect(link)
    else:
        return redirect('/no-access/tariff-plans')

@main.route('/my/profile')
@token_required
def my_profile():
    userid = request.user_id
    user = get_user_by_id(userid)
    place = get_place_by_osm(user.address)
    page = request.page
    datapage = get_page_by_id(page)
    role = request.role
    datarole = get_role_by_id(role)
    personal_tree = get_parents_list_by_id(datapage.tree_id)
    tickets = get_user_tickets_all(userid)
    return render_template('main/profile.html', page=datapage.title, tickets=tickets, treelist=personal_tree[::-1], user=user, place=place, role=datarole)

@main.route('/my/profile/edit')
@token_required
def my_profile_edit():
    userid = request.user_id
    user = get_user_by_id(userid)
    place = get_place_by_osm(user.address)
    page = request.page
    datapage = get_page_by_id(page)
    role = request.role
    datarole = get_role_by_id(role)
    personal_tree = get_parents_list_by_id(datapage.tree_id)
    tickets = get_user_tickets_all(userid)
    return render_template('main/profile-edit.html', page=datapage, tickets=tickets, treelist=personal_tree[::-1],
                           user=user, place=place, role=datarole)

@main.route('/my/profile/edit/save', methods=['POST'])
@token_required
def my_profile_edit_save():
    userid = request.user_id
    country = request.form.get('country')
    address = request.form.get('osm')
    page = request.form.get('page')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    print(first_name)
    user = create_or_update_user(
        id=userid,
        country=country,
        address=address,
        first_name=first_name,
        last_name=last_name,
        page=page,
    )
    token = update_login_token(userid)
    response = make_response(redirect(url_for('main.my_profile')))
    response.set_cookie('token', user['token'], domain='.atatek.kz')
    # response.set_cookie('token', token['token'])
    return response

@main.route('/my/profile/ticket/<int:id>')
@token_required
def my_profile_ticket(id):
    userid = request.user_id
    user = get_user_by_id(userid)
    place = get_place_by_osm(user.address)
    page = request.page
    personal_tree = get_parents_list_by_id(get_page_by_id(page).tree_id)
    tickets = get_user_ticket_by_id(id)
    return render_template('main/ticket.html', ticket=tickets, treelist=personal_tree, user=user, place=place)

@main.route('/no-access/tariff-plans')
@token_required
def no_access():
    page = request.page
    roles = get_all_roles()
    print(roles)
    return render_template('main/no-access.html',page=get_page_by_id(page), roles=roles)


@main.route('/my/family')
@token_required
def family():
    with open(family_path, 'r', encoding='utf-8') as file:
        settings = json.load(file)
    page = request.page
    role = request.role
    user = request.user_id
    if check_user_family(user):
        readonly = False
        count = get_tree_count(user)

        if role == 1:
            userAccess = get_role_by_id(role)
            if userAccess.family_person_count > count:
                readonly = True
        if role == 2 or role == 3 or role == 4:
            userAccess = get_active_subs_by_id(user)

            if userAccess is not None and userAccess.family_person_count > count:
                readonly = True
        if role == 5:
            readonly = True
        print(readonly)

        return render_template('family/main.html', page=get_page_by_id(page), set=settings, readOnlyData=readonly)
    else:
        return render_template('family/start.html', page=get_page_by_id(page), set=settings)


@main.route('/my/family/get/my')
@token_required
def family_get():
    user = request.user_id
    family = get_my_tree(user)
    return family

@main.route('/my/family/start', methods=['POST'])
@token_required
def start_family():
    user = request.user_id
    data = request.form
    gf = create_record_for_table(
        name=data['gf_first_name'] + ' ' + data['gf_last_name'],
        birthday=data['gf_birth_date'],
        alive=True if data['gf_alive'] == 'alive' else False,
        death=data['gf_death_date'] if 'gf_death_date' in data else None,
        created_by=user,
        gender='male',
    )
    gm = create_record_for_table(
        name=data['gm_first_name'] + ' ' + data['gm_last_name'],
        birthday=data['gm_birth_date'],
        alive=True if data['gm_alive'] == 'alive' else False,
        death=data['gm_death_date'] if 'gm_death_date' in data else None,
        pids=gf.id,
        created_by=user,
        gender='female',
    )
    father = create_record_for_table(
        name=data['father_first_name'] + ' ' + data['father_last_name'],
        birthday=data['father_birth_date'],
        alive=True if data['father_alive'] == 'alive' else False,
        death=data['father_death_date'] if 'father_death_date' in data else None,
        fid=gf.id,
        mid=gm.id,
        created_by=user,
        gender='male',
    )
    mother = create_record_for_table(
        name=data['mother_first_name'] + ' ' + data['mother_last_name'],
        birthday=data['mother_birth_date'],
        alive=True if data['mother_alive'] == 'alive' else False,
        death=data['mother_death_date'] if 'mother_death_date' in data else None,
        pids=father.id,
        created_by=user,
        gender='female',
    )
    update_record_for_table(gf.id, gm.id)
    update_record_for_table(father.id, mother.id)
    userData = get_user_by_id(user)
    return redirect(url_for('main.family'))

@main.route('/my/family/update/my', methods=['POST'])
@token_required
def update_family():
    user = request.user_id
    # Получаем JSON-данные из тела запроса
    data = request.get_json()

    # Проверяем, получены ли данные
    if not data:
        return jsonify({"error": "No data provided"}), 400

    add = data.get('add', [])
    update = data.get('update', [])
    remove = data.get('remove', [])

    add = add[::-1]
    last = None
    print(remove)
    for item in add:
        id = item.get('id')
        gender = item.get('gender')
        mid = item.get('mid', None)
        fid = item.get('fid', None)
        pids = item.get('pids', None)

        adder = create_record_by_ui(
            gender=gender,
            mid=mid,
            fid=fid,
            pids=pids,
            created_by=user,
            bid=id,
        )
    for item in update:
        id = item.get('id')
        name = item.get('name')
        gender = item.get('gender')
        birthday = item.get('birthday')
        mid = item.get('mid', None)
        fid = item.get('fid', None)
        pids = item.get('pids', None)
        alive = True if item.get('alive') == 'true' else False
        updater = update_record_by_ui(
            id=id,
            name=name,
            gender=gender,
            birthday=birthday,
            mid=mid,
            fid=fid,
            pids=pids,
            alive=alive
        )
        print(alive)
    removeS = remove_node_by_id(remove)

    # Возвращаем полученные данные в формате JSON для проверки
    return jsonify({
        "user_id": user,
        "received_data": data
    }), 200