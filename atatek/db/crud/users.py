from sqlalchemy import false
from atatek.utils import hash_password, check_password, generate_jwt

from atatek.db import db, User, Referral, Verify
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