from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from server import users
from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check if username exists in database
        user_json = users.find_one({"username": username})
        if user_json:
            # if check_password_hash(user_json['password'], password):
            if user_json['password'] == password:
                flash('Logged in successfully!', category='success')
                user = User(user_json)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            # if username does not exist, redirect to signup page
            flash('Username does not exist.', category='error')
            return redirect(url_for('auth.signup'))

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')  # Gets the username from the form
        password1 = request.form.get('password1')  # Gets the password from the form
        password2 = request.form.get('password2')

        # check if username exists in database
        user = users.find_one({"username": username})
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 2:
            flash('Username too short.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # Add new user to database
            user_json = {
                "username": username,
                # "password": generate_password_hash(password1, method='pbkdf2:sha256'),
                "password": password1,
                "records": [],
                "bricks": {}
            }
            users.insert_one(user_json)
            new_user = User(user_json)
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
