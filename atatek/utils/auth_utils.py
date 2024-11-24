import random
import string
import bcrypt
import jwt
import datetime

# Секретный ключ для JWT
SECRET_KEY = "atatek"

# 1. Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# 2. Расшифровка пароля
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())  # Преобразуйте хеш в байты


# 3. Генерация JWT токена
def generate_jwt(user_id, first_name, last_name, role, page) -> str:
    payload = {
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'role': role,
        'page': page,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Время истечения 1 час
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(token)
    return token

# 4. Проверка JWT токена
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def generate_unique_id(length=9):
    characters = string.ascii_letters + string.digits  # Включаем большие и маленькие буквы, а также цифры
    return ''.join(random.choice(characters) for _ in range(length))
