from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        submitted_data = request.get_json(force=True)
        submitted_req = submitted_data['req']
        submitted_name = submitted_data['name']
        submitted_password = submitted_data['password']
        if submitted_req != 1 and submitted_req != 2:
            return jsonify({'response':'Neredaguokite puslapio.</br>Perkraukite puslapį.'})
        #Jeigu registruojasi:
        elif submitted_req == 1:
            user = User.query.filter_by(name=submitted_name).first()
            if user:
                return jsonify({'response':'Vartotojas jau egzistuoja</br>Perkraukite puslapį'})
            else:
                if len(submitted_name) > 150:
                    return jsonify({'response':'Vartotojo vardas per ilgas.'})
                if len(submitted_password) > 150:
                    return jsonify({'response':'Slaptažodis per ilgas.'})
                new_user = User(name=submitted_name,password=generate_password_hash(submitted_password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                return jsonify({'response':1})     
        #Jeigu jungiasi:
        elif submitted_req == 2:
            user = User.query.filter_by(name=submitted_name).first()
            if user:
                if check_password_hash(user.password,submitted_password):
                    login_user(user,remember=True)
                    return jsonify({'response':1})
                else:
                    return jsonify({'response':'Neteisingas slaptažodis arba elektroninis paštas.'})
            else:
                return jsonify({'response':'Neteisingas slaptažodis arba elektroninis paštas.'})

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))