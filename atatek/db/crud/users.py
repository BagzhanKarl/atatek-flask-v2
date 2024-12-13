from sqlalchemy import false
from atatek.utils import hash_password, check_password, generate_jwt

from atatek.db import db, User, Referral, Verify, Subscription, Role
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_or_update_user(id=None, phone=None, role=None, first_name=None, last_name=None, password=None, country=None, address=None, page=None):
    try:
        if id:
            print('Обновление данных')
            user = User.query.filter_by(id=id).first()
            if user:
                print('Успешно')
                if country: user.country = country
                if address: user.address = address
                if page: user.page = page
                if role: user.role = role
                db.session.commit()
                return {"status": True, "user": user.id}
        else:
            print('Добавление данных')
            # Шаг создания нового пользователя
            if phone:
                existing_user = User.query.filter_by(phone=phone).first()
                if existing_user:
                    print('Номер уже есть')

                    return {"status": False, "data": "Бұл номермен басқа қолданушы тіркелген!"}
                user = User(
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name,
                    password=hash_password(password)
                )
                db.session.add(user)
                db.session.commit()
                print('Успешно')
                return {"status": True, "user": user.id}
    except IntegrityError:
        db.session.rollback()
        return {"status": False, "data": "Деректерді сақтау кезінде қателік болды, кейінірек қайталап көріңіз"}
    except Exception as e:
        db.session.rollback()
        print(f"Произошла ошибка: {str(e)}")
        return {"status": False, "data": "Деректерді сақтау кезінде қателік болды, кейінірек қайталап көріңіз"}

def login_user(phone, password):
    try:
        user = User.query.filter_by(phone=phone).first()
        if user is None:
            return {"status": False, "data": "Пользователь с таким номером не найден"}

        if check_password(password, user.password) == True:
            token = generate_jwt(user.id, user.first_name, user.last_name, user.role, user.page)
            return {"status": True, "token": token}
        else:
            return {"status": False, "data": "Телефон номер немесе құпиясөзіңіз қате"}

    except Exception as e:
        print(e)
        return {"status": False, "data": "Деректерді өңдеу кезінде қателік болды, кейінірек қайталаңыз"}

# Get User by ID
def get_user_by_id(user_id):
    return User.query.get(user_id)

# Get User by Phone
def get_user_by_phone(phone):
    return User.query.filter_by(phone=phone).first()

# Update User
def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return user
    return None

# Deactivate User
def deactivate_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = False
        db.session.commit()
        return user
    return None

# Create Referral
def create_referral(referrer_id, referred_id):
    try:
        referral = Referral(referrer_id=referrer_id, referred_id=referred_id)
        db.session.add(referral)
        db.session.commit()
        return referral
    except IntegrityError:
        db.session.rollback()
        return None

# Get Referral by Referrer and Referred
def get_referral_by_user_ids(referrer_id, referred_id):
    return Referral.query.filter_by(referrer_id=referrer_id, referred_id=referred_id).first()

# Get Referrals by Referrer
def get_referrals_by_referrer(referrer_id):
    return Referral.query.filter_by(referrer_id=referrer_id).all()

# Verify User (Create Verification Code)
def create_verification(user_id, code):
    verification = Verify(user=user_id, code=code)
    db.session.add(verification)
    db.session.commit()
    return verification

# Get Verification by User ID
def get_verification_by_user(user_id):
    return Verify.query.filter_by(user=user_id).order_by(Verify.created_at.desc()).first()

# Delete Referral
def delete_referral(referral_id):
    referral = Referral.query.get(referral_id)
    if referral:
        db.session.delete(referral)
        db.session.commit()
        return referral
    return None

# Delete User (Cascade Deletion)
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user
    return None

def get_all_user_list():
    return User.query.all()

def get_all_moderator_list():
    return User.query.filter_by(role=4).all()


def create_subscription(user_id, role_id):
    print(user_id, role_id)

    # Обновляем или создаем пользователя для всех ролей
    create_or_update_user(id=user_id, role=role_id)

    # Проверяем, есть ли активная подписка
    subs_to_delete = Subscription.query.filter_by(user=user_id, is_active=True).first()
    if subs_to_delete:
        print('Есть запись, которую нужно удалить')
        db.session.delete(subs_to_delete)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при удалении подписки: {e}")
            return False

    print(f"role_id: {role_id}")  # Проверяем значение role_id
    if int(role_id) == 2 or int(role_id) == 3:
        print("Создаем запись для подписки")
        # Остальной код

        role = Role.query.get(role_id)
        if not role:
            print(f"Роль с id {role_id} не найдена!")
            return False

        subs = Subscription(
            user=user_id,
            role=role.id,
            addchild=role.add_child,
            addinfo=role.add_info,
            personal=role.personal_page,
            allpage=role.all_pages,
            family_person_count=role.family_person_count,
            days=30,
            is_active=True
        )
        db.session.add(subs)
        try:
            db.session.commit()
            print("Запись подписки успешно создана!")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при сохранении подписки: {e}")
            return False

    return True  # Возвращаем True, если обновление прошло успешно



def get_active_subs_by_id(user_id):
    subs = Subscription.query.filter_by(user=user_id, is_active=True).first()
    if subs:
        return Subscription.query.filter_by(user=user_id, is_active=True).first()
    else:
        return None

def update_subs(subs_id, addchild=None, addinfo=None, personal=None, allpage=None, family_person_count=None):
    subs = Subscription.query.get(subs_id)
    if subs:
        subs.addchild = addchild if addchild is not None else subs.addchild
        subs.addinfo = addinfo if addinfo is not None else subs.addinfo
        subs.personal = True if personal == "on"  else False
        subs.allpage = True if allpage == "on"  else False
        subs.family_person_count = family_person_count if family_person_count is not None else subs.family_person_count
        db.session.commit()
        return True
    else:
        return False