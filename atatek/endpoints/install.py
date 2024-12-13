from flask import Blueprint, jsonify

from atatek.db import create_role, create_tree, create_new_page, get_all_roles

install = Blueprint('install', __name__)

@install.route('/install/first/launch')
def first_launch():
    roles =  [
        {
          "add_child": 0,
          "add_info": 0,
          "all_pages": False,
          "family_person_count": 10,
          "personal_page": True,
          "price": 0,
          "titile": "Бастау"
        },
        {
          "add_child": 0,
          "add_info": 0,
          "all_pages": False,
          "family_person_count": 15,
          "personal_page": True,
          "price": 0,
          "titile": "Сарапшы"
        },
        {
          "add_child": 10,
          "add_info": 10,
          "all_pages": True,
          "family_person_count": 10,
          "personal_page": True,
          "price": 15000,
          "titile": "Алтын"
        },
        {
          "add_child": 0,
          "add_info": 0,
          "all_pages": False,
          "family_person_count": 0,
          "personal_page": True,
          "price": 0,
          "titile": "Модератор"
        },
        {
          "add_child": 0,
          "add_info": 0,
          "all_pages": False,
          "family_person_count": 0,
          "personal_page": True,
          "price": 0,
          "titile": "Администратор"
        }
    ]
    for role in roles:
        data = create_role(
            title=role["titile"],
            price=role["price"],
            add_child=role["add_child"],
            add_info=role["add_info"],
            all_pages=role["all_pages"],
            personal_page=role["personal_page"],
            family_person_count=role["family_person_count"],
        )
        print(data)
    return jsonify(roles)

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