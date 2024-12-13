from atatek.db import db, Role
from sqlalchemy.exc import IntegrityError

# Create Role
def create_role(title, price, add_child=None, add_info=None, all_pages=None, family_person_count=None,
                personal_page=None):

    role = Role(
        title=title,
        price=price,
        add_child=add_child,
        add_info=add_info,
        all_pages=all_pages,
        family_person_count=family_person_count,
        personal_page=personal_page

    )
    db.session.add(role)
    db.session.commit()
    return role


# Get Role by ID
def get_role_by_id(role_id):
    return Role.query.get(role_id)

# Get Role by Title
def get_role_by_title(title):
    return Role.query.filter_by(title=title).first()

# Get All Roles
def get_all_roles():
    return Role.query.all()

# Update Role
def update_role(role_id, add_child=None, add_info=None, price=None, title=None, family_person_count=None, personal=False, all_pages=False):
    role = Role.query.get(role_id)
    if role:
        if add_child: role.add_child = add_child
        if add_info: role.add_info = add_info
        if price: role.price = price
        if title: role.title = title
        if personal: role.personal = personal
        if all_pages: role.all_pages = all_pages
        if family_person_count: role.family_person_count = family_person_count
        db.session.commit()
        return role
    return None

# Delete Role
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return role
    return None
