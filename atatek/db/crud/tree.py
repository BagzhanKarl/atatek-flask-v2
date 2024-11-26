from datetime import datetime
from atatek.db import db, Tree, TreeInfo
from sqlalchemy.exc import IntegrityError

from atatek.utils import get_tree_data_on_request


# Создание нового дерева
def create_tree(name, item_id, birth=None, death=None,  parent_id=None, created_by=None, updated_by=None):
    try:
        tree = Tree(
            name=name,
            birth=birth,
            death=death,
            parent_id=parent_id,
            created_by=created_by,
            updated_by=updated_by,
            item_id=item_id,
            status=False
        )
        db.session.add(tree)
        db.session.commit()
        print('Сохранено')
        return tree
    except IntegrityError as e:
        db.session.rollback()
        print(f"Ошибка IntegrityError: {e.orig}")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"Произошла ошибка: {str(e)}")
        return None

def get_childs_by_parent(parent_id: int, role):
    childs = Tree.query.filter_by(parent_id=parent_id).all()
    response = []
    if childs:
        for child in childs:
            info = TreeInfo.query.filter_by(tree_id=child.id).first()
            infoData = False
            if info:
                infoData = True

            response.append({
                'id': child.id,
                'name': child.name,
                'untouchable': False,
                'role': role,
                'birth': child.birth,
                'death': child.death,
                'parent_id': child.parent_id,
                'info': infoData
            })
        return response
    else:
        item = Tree.query.filter_by(id=parent_id).first()
        data = get_tree_data_on_request(item.item_id)
        for item in data:
            exsist = Tree.query.filter_by(item_id=item['id']).first()
            if not exsist:
                item_data = create_tree(
                    name=item['name'],
                    item_id=item['id'],
                    parent_id=parent_id,
                    birth=item['birth_year'],
                    death=item['death_year'],
                    created_by=None,
                )
                response.append({
                    "id": item_data.id,
                    "name": item_data.name,
                    "untouchable": False,
                    "role": role,
                    "birth": item_data.birth,
                    "death": item_data.death,
                    "parent_id": item_data.parent_id,
                    "info": False,
                })
        return response

def read_tree_by_id(id):
    tree = Tree.query.filter_by(id=id).first()
    return tree

def read_tree_info_by_id(id):
    tree = TreeInfo.query.filter_by(tree_id=id).first()
    return tree

def delete_tree(id):
    tree = Tree.query.filter_by(id=id).first()
    db.session.delete(tree)
    db.session.commit()
    return True

def edit_tree_crud(id: int, name: str, birth=None, death=None, updated_by=None):
    tree = Tree.query.filter_by(id=id).first()
    tree.name = name
    tree.birth = birth
    tree.death = death
    tree.updated_by = updated_by
    db.session.commit()
    return True

def create_or_update_tree_info(tree: int, info: str, tree_icon=None, tree_full_icon=None, created_by=None, updated_by=None):
    existing_tree = TreeInfo.query.filter_by(tree_id=tree).first()

    if existing_tree:
        # Обновляем информацию в существующей записи
        existing_tree.info = info
        existing_tree.tree_icon = tree_icon
        existing_tree.tree_full_icon = tree_full_icon
        existing_tree.updated_by = updated_by
    else:
        # Создаем новую запись
        tree_info = TreeInfo(
            tree_id=tree,
            info=info,
            tree_icon=tree_icon,
            tree_full_icon=tree_full_icon,
            created_by=created_by,
            updated_by=updated_by,
        )
        db.session.add(tree_info)

    db.session.commit()
    return True

def get_parents_list_by_id(id, lastTouch=None):
    item = id
    parents = []
    while True:
        start = db.session.query(Tree).filter_by(id=item).first()
        if not start:
            break  # Если элемент не найден, выходим из цикла

        treeinfo = db.session.query(TreeInfo).filter_by(tree_id=start.id).first()

        # Добавляем элемент в список
        parents.append({
            "id": start.id,
            "name": start.name,
            "untouchable": False if start.id == id and lastTouch else True,
            "gender": 'M',
            "status": 'notmy',
            "born": None,
            "death": None,
            "info": True if treeinfo else False,
            "parent": start.parent_id if start.parent_id is not None else "",  # Заменить на пустую строку, если родитель не найден
        })

        # Переход к родителю
        parent = db.session.query(Tree).filter_by(id=start.parent_id).first()
        if parent:
            item = parent.id
        else:
            break  # Если родителя нет, выходим из цикла


    return parents
