from bson import ObjectId
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from server import users
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import ADMIN, ADMIN_PASSWORD

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check if user is admin
        if username == ADMIN and password == ADMIN_PASSWORD:
            flash('Welcome!', category='success')
            admin_json = users.find_one({"username": ADMIN})
            admin = User(admin_json)
            login_user(admin, remember=True)
            return redirect(url_for('admin.dashboard'))
        # check if username exists in database
        user_json = users.find_one({"username": username})
        if user_json:
            if check_password_hash(user_json['password'], password):
                # if user_json['password'] == password:
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
                "password": generate_password_hash(password1, method='pbkdf2:sha256'),
                # "password": password1,
                "records": [],
                "bricks": {}
            }
            users.insert_one(user_json)
            new_user = User(user_json)
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'reset_username' in request.form:
            return reset_username()
        elif 'reset_password' in request.form:
            return reset_password()
    user_id = current_user.get_id()
    user_name = users.find_one({"_id": ObjectId(user_id)})['username']
    return render_template('profile.html', user=current_user, user_name=user_name)


@auth.route('/reset-username', methods=['GET', 'POST'])
@login_required
def reset_username():
    if request.method == 'POST':
        user_json = users.find_one({"_id": ObjectId(current_user.get_id())})
        if user_json:
            old_username = user_json['username']
            new_username = request.form.get('new_username')
            if old_username == new_username:
                flash('Username unchanged.', category='error')
            elif users.find_one({"username": new_username}):
                flash('Username already exists.', category='error')
            elif len(new_username) < 2:
                flash('Username too short.', category='error')
            else:
                users.update_one(
                    {"_id": ObjectId(current_user.get_id())},
                    {"$set": {"username": new_username}}
                )
                flash('Username changed!', category='success')
                # Update the current_user
                user_json = users.find_one({"_id": ObjectId(current_user.get_id())})
                user = User(user_json)
                login_user(user, remember=True)
                return redirect(url_for('auth.profile'))
        else:
            flash('Please login again.', category='error')
            return redirect(url_for('auth.login'))

    return redirect(url_for('auth.profile'))


@auth.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        flash('Trying to reset password...', category='success')
        old_password = request.form.get('old_password')
        user_json = users.find_one({"_id": ObjectId(current_user.get_id())})
        if user_json:
            if check_password_hash(user_json['password'], old_password):
                new_password1 = request.form.get('new_password1')
                new_password2 = request.form.get('new_password2')
                if new_password1 != new_password2:
                    flash('Passwords don\'t match.', category='error')
                elif len(new_password1) < 8:
                    flash('Password must be at least 8 characters.', category='error')
                else:
                    users.update_one(
                        {"_id": ObjectId(current_user.get_id())},
                        {"$set": {"password": generate_password_hash(new_password1, method='pbkdf2:sha256')}}
                    )
                    flash('Password changed!', category='success')
                    # Update the current_user
                    user_json = users.find_one({"_id": ObjectId(current_user.get_id())})
                    user = User(user_json)
                    login_user(user, remember=True)
                    return redirect(url_for('auth.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Please login again.', category='error')
            return redirect(url_for('auth.login'))

    return redirect(url_for('auth.profile'))
