from atatek.db import db, Pages, PopularPeople, Moderators
from sqlalchemy.exc import IntegrityError

def create_new_page(title, juz, breed1, breed2, breed3, tree):
    if juz == 'Ұлы жүз':
        domain = 'https://uly-jyz.atatek.kz/'
    elif juz == 'Орта жүз':
        domain = 'https://orta-jyz.atatek.kz/'
    elif juz == 'Кіші жүз':
        domain = 'https://kishi-jyz.atatek.kz/'
    elif juz == 'Жүзден тыс':
        domain = 'https://jyzden-tys.atatek.kz/'
    page = Pages(
        title=title,
        juz=juz,
        breed1=breed1,
        breed2=breed2,
        breed3=breed3,
        tree_id=tree,
        subdomain=domain,
    )
    db.session.add(page)
    db.session.commit()
    return page


def get_page_by_id(page_id):
    page = Pages.query.get(page_id)
    return page

def get_page_by_breeds(breed1, breed2, breed3):
    page = Pages().query.filter_by(breed1=breed1, breed2=breed2, breed3=breed3).first()
    return page

def get_all_pages():
    pages = Pages.query.all()
    return pages

def get_moderator_list_by_page_id(id):
    moderators = Moderators.query.filter_by(page=id).all()
    return moderators

def create_moderator(id, page):
    # Проверяем, существует ли запись с таким user_id и page
    existing_moderator = Moderators.query.filter_by(user_id=id, page=page).first()
    if existing_moderator:
        return existing_moderator  # Возвращаем существующего модератора, если он найден

    # Если не найден, создаем нового
    moderator = Moderators(
        user_id=id,
        page=page
    )
    db.session.add(moderator)
    db.session.commit()
    return moderator

def delete_moderator(user_id):
    # Находим модератора с указанным user_id и page
    moderator = Moderators.query.filter_by(id=user_id).first()
    if not moderator:
        return False  # Модератор с такими данными не найден

    # Удаляем модератора
    db.session.delete(moderator)
    db.session.commit()
    return True  # Удаление успешно

def add_popular_person(fullname, page, image, content, birthday=None):
    person = PopularPeople(
        fullname=fullname,
        image=image,
        content=content,
        birthday=birthday,
        page=page

    )
    db.session.add(person)
    db.session.commit()
    return person

def get_all_popular_persons_by_page_id(page_id):
    popular_persons = PopularPeople.query.filter_by(page=page_id).all()
    return popular_persons


def get_one_popular_person_by_id(id):
    popular_person = PopularPeople.query.filter_by(id=id).first()
    return popular_person