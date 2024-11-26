from flask import Blueprint, render_template, url_for, request, redirect, session, make_response

from atatek.db import get_all_pages, get_parents_list_by_id
from atatek.db.crud.users import create_or_update_user, create_referral, login_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = login_user(phone, password)
        print(user['status'])
        if user['status'] == True:
            response = make_response(redirect(url_for('main.index')))
            # Устанавливаем куки для всех поддоменов
            # response.set_cookie('token', user['token'], domain='.atatek.kz')
            response.set_cookie('token', user['token'])
            return response
        else:
            return render_template('auth/login.html', errorText=user['data'])


    else:
        return render_template('auth/login.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(redirect(url_for('auth.login')))
    res.set_cookie('token', 'bumchakachaka', max_age=0)
    return res

@auth.route('/register/user', defaults={'inviter_id': None}, methods=['GET', 'POST'])
@auth.route('/register/user/<int:inviter_id>', methods=['GET', 'POST'])
def register_user(inviter_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone']
        password = request.form['password']
        user = create_or_update_user(
            phone=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        print(user)
        if user['status'] == True:
            session['user_id'] = user['user']
            if inviter_id:
                inviter = create_referral(inviter_id, user['user'])
                print(f"User invited by ID: {inviter}")
            return redirect(url_for('auth.register_address'))
        else:
            render_template('auth/user.html', errorText=user['data'])
    else:
        return render_template('auth/user.html')

@auth.route('/register/address', methods=['GET', 'POST'])
def register_address():
    if request.method == 'POST':
        user_id = session['user_id']
        country = request.form['country']
        address = request.form['osm']
        user = create_or_update_user(
            id=user_id,
            country=country,
            address=address
        )
        if user['status'] == True:
            return redirect(url_for('auth.register_site'))
        else:
            return render_template('auth/address.html', errorText=user['data'])

    else:
        return render_template('auth/address.html')

@auth.route('/register/site', methods=['GET', 'POST'])
def register_site():
    if request.method == 'POST':
        user_id = session['user_id']
        page = request.form['page']
        user = create_or_update_user(
            id=user_id,
            page=page
        )
        if user['status'] == True:
            return redirect(url_for('auth.register_verify'))
        else:
            return render_template('auth/sites.html', errorText=user['data'])

    else:
        page = get_all_pages()
        pageList = []
        for item in page:
            parents = get_parents_list_by_id(item.tree_id)
            search = ''
            for parent in parents:
                search += parent['name'] + " "
            pageList.append({
                'id': item.id,
                'title': item.title,
                'search': search
            })
        return render_template('auth/sites.html', pages=pageList)

@auth.route('/register/verify', methods=['GET', 'POST'])
def register_verify():
    return redirect(url_for('auth.login'))
