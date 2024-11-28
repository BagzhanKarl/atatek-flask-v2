from flask import Blueprint, jsonify

from atatek.db import create_role, create_tree, create_new_page

install = Blueprint('install', __name__)

@install.route('/install/first/launch')
def first_launch():
    # create first tree data
    roles = [
        {
            "title": "Бастау",
            "price": 0.00,
            "addchild": 0,
            "addinfo": 0,
        },
        {
            "title": "Сарапшы",
            "price": 0.00,
            "addchild": 0,
            "addinfo": 0,
        },
        {
            "title": "Алтын",
            "price": 0.00,
            "addchild": 0,
            "addinfo": 0,
        },
        {
            "title": "Модератор",
            "price": 0.00,
            "addchild": 0,
            "addinfo": 0,
        },
        {
            "title": "Администратор",
            "price": 0.00,
            "addchild": 0,
            "addinfo": 0,
        },
    ]
    for role in roles:
        role = create_role(
            title=role["title"],
            price=role["price"],
            add_child=role["addchild"],
            add_info=role["addinfo"],
        )

    return jsonify(
        {
            "status": True,
        }
    )

@install.route('/install/second/launch')
def second_launch():
    tree = create_tree(
        name='Алаш',
        item_id=14
    )
    return jsonify(
        {
            "status": True,
        }
    )

@install.route('/install/open/page/for/<int:id>')
def open_page(id):
    page = create_new_page(
        title='Жарты',
        juz='Ұлы жүз',
        breed1='alban',
        breed2='sary',
        breed3='zharty',
        tree=id
    )