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


def create_record_for_table(name=None, gender=None, user=None, birthday=None, death=None, alive=True, pids=None, fid=None, mid=None, created_by=None):
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
        created_by=created_by
    )
    db.session.add(new_record)
    db.session.commit()
    return new_record

def update_record_for_table(id, pids):
    record = Family.query.get(id)
    record.pids = pids
    db.session.commit()

def get_my_tree(user):
    family = Family.query.filter_by(created_by=user).all()
    result = []
    for item in family:
        formatted_birthday = datetime.strptime(item.birthday, "%Y-%m-%d").strftime(
            "%d.%m.%Y") if item.birthday else None
        formatted_death = datetime.strptime(item.death, "%Y-%m-%d").strftime("%d.%m.%Y") if item.death else None
        result.append({
            "id": item.id,
            "name": item.name ,
            "pids": item.pids if isinstance(item.pids, list) else [item.pids] if item.pids else None,
            "gender": item.gender,
            "birthday": formatted_birthday,
            "death": formatted_death,
            "fid": item.fid if item.fid else None,
            "mid": item.mid if item.mid else None,
        })
    return result
