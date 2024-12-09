import json
from datetime import datetime

from atatek.db import db, Family
from sqlalchemy.exc import IntegrityError


def check_user_family(user_id):
    exist_family = Family.query.filter_by(created_by=user_id).first()
    if exist_family:
        return True
    else:
        return False


def create_record_for_table(name=None, bid=None, gender=None, user=None, birthday=None, death=None, alive=True, pids=None, fid=None, mid=None, created_by=None):
    new_record = Family(
        name=name,
        birthday=birthday,
        death=death,
        alive=alive,
        pids=pids,
        fid=fid,
        mid=mid,
        user=user,
        gender=gender,
        created_by=created_by,
        bid=bid
    )
    db.session.add(new_record)
    db.session.commit()
    return new_record

def update_record_for_table(id, pids):
    record = Family.query.get(id)
    record.pids = pids
    db.session.commit()


from datetime import datetime
from sqlalchemy.orm import aliased

from datetime import datetime


def get_my_tree(user):
    family = Family.query.filter_by(created_by=user).all()
    result = []

    for item in family:
        data = item.pids
        pids = [x.strip() for x in data.split(',')] if data else []

        # Сортировка детей по дате рождения
        children = []
        if pids:
            for pid in pids:
                child = Family.query.get(pid)
                if child:
                    child_birthday = datetime.strptime(child.birthday, "%Y-%m-%d") if child.birthday else None
                    children.append((child, child_birthday))

            # Сортируем детей по дате рождения (если дата указана)
            children.sort(key=lambda x: x[1] if x[1] else datetime.max)

            pids = [child[0].id for child in children]

        result.append({
            "id": item.id,
            "name": item.name,
            "pids": pids,
            "gender": item.gender,
            "birthday": item.birthday,
            "death": item.gender,
            "alive": item.alive,
            "fid": item.fid if item.fid else None,
            "mid": item.mid if item.mid else None,
        })

    return result

def get_tree_count(user):
    count = Family.query.filter_by(created_by=user).count()
    return count


def create_record_by_ui(name=None, bid=None, gender=None, user=None, birthday=None, death=None, alive=True, pids=None, fid=None, mid=None, created_by=None):
    if isinstance(mid, str) and mid:  # Проверяем, что mid является строкой и не пустой
        mother = Family.query.filter_by(bid=mid).first()

        if mother:  # Убедимся, что результат запроса не None
            mid = mother.id

    if isinstance(fid, str) and fid:
        father = Family.query.filter_by(bid=fid).first()
        if father: fid = father.id
        else:
            father = Family.query.filter_by(id=fid).first()
            fid = father.id



    new_record = Family(
        name=name,
        birthday=birthday,
        death=death,
        gender=gender,
        user=user,
        alive=alive,
        bid=bid,
        pids=pids,
        fid=fid,
        mid=mid,
        created_by=created_by,
    )
    db.session.add(new_record)

    db.session.commit()
    return new_record


def update_record_by_ui(id=None, name=None, bid=None, gender=None, birthday=None, death=None, alive=True, pids=None,
                        fid=None, mid=None, created_by=None):
    piddata = []  # Список для хранения id
    for pid in pids:
        if pid.isdigit():  # Если pid — число, добавляем его сразу
            piddata.append(pid)
        else:  # Иначе ищем в базе
            partner = Family.query.filter_by(bid=pid).first()
            if partner:  # Проверяем, найден ли партнер
                piddata.append(str(partner.id))  # Добавляем id как строку

    pid = ', '.join(piddata) if piddata else None  # Преобразуем список в строку (или None, если список пуст)

    # Получаем запись из базы
    record = Family.query.get(id)

    # Обновляем поля, если переданы новые значения
    record.name = name if name else record.name
    record.bid = bid if bid else record.bid
    record.gender = gender if gender else record.gender
    record.birthday = birthday if birthday else record.birthday
    record.death = death if death else record.death
    record.pids = pid if pids else record.pids
    record.fid = fid if fid else record.fid
    record.mid = mid if mid else record.mid

    record.alive = alive
    print(alive)
    db.session.commit()
