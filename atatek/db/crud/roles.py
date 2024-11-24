from atatek.db import db, Role
from sqlalchemy.exc import IntegrityError

# Create Role
def create_role(title, price, add_child=False, add_info=False):
    try:
        role = Role(
            title=title,
            price=price,
            add_child=add_child,
            add_info=add_info
        )
        db.session.add(role)
        db.session.commit()
        return role
    except IntegrityError:
        db.session.rollback()
        return None

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
def update_role(role_id, **kwargs):
    role = Role.query.get(role_id)
    if role:
        for key, value in kwargs.items():
            setattr(role, key, value)
        role.updated_at = datetime.utcnow()
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
