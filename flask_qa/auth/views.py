import imp
from flask import Blueprint, redirect, render_template, url_for, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from ..models.user import User
from ..utils import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name = name).first()
        error_message = ''

        if not user or not check_password_hash(user.password, password):
            error_message = 'Could not login. Please checkand try again. '

        if not error_message:
            login_user(user)
            return redirect(url_for('q_a.index'))
    return render_template('login.html')


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        unhashed_password = request.form['password']

        user = User(
            name = name, 
            unhashed_password = unhashed_password, 
            admin = False, 
            expert = False
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('auth.login'))