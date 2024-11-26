import json
import os
from flask import Blueprint, render_template, request, redirect

from atatek.db import User, get_place_by_osm, get_parents_list_by_id, get_page_by_id, get_user_tickets_all, \
    get_user_ticket_by_id, get_all_roles
from atatek.db.crud.users import get_user_by_id
from atatek.utils import token_required

main = Blueprint('main', __name__)
settings_path = os.path.join(os.path.dirname(__file__), '../utils/settings.json')

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

@main.route('/my')
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
    personal_tree = get_parents_list_by_id(get_page_by_id(page).tree_id)
    tickets = get_user_tickets_all(userid)
    return render_template('main/profile.html', page=get_page_by_id(page).title, tickets=tickets, treelist=personal_tree, user=user, place=place)

@main.route('/my/profile/edit')
def my_profile_edit():
    pass

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