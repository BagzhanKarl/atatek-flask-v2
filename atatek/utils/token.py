from functools import wraps
from flask import request, make_response, redirect
from atatek.utils import verify_jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            response = make_response(redirect('/auth/login'))
            return response
        payload = verify_jwt(token)
        if(payload):
            request.user_id = payload['user_id']
            request.first_name = payload['first_name']
            request.last_name = payload['last_name']
            request.role = payload['role']
            request.page = payload['page']
        else:
            response = make_response(redirect('/auth/login'))
            return response
        return f(*args, **kwargs)
    return decorated


def api_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if token:
            payload = verify_jwt(token)
            if payload:
                # Извлекаем данные из токена и добавляем их в объект request
                request.role = payload.get('role', 1)  # Если role нет, берем 1
                return f(*args, **kwargs)

        # Если токена нет или он недействителен
        request.role = 1
        return f(*args, **kwargs)

    return decorated