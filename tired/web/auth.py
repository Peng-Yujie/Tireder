from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from . import user_collection
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check if username exists in database
        user = user_collection.find_one({"username": username})
        if user:
            # check if password is correct
            if check_password_hash(user['password'], password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", text="text")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("logout.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # TODO: send data to database
    if request.method == 'POST':
        username = request.form.get('username')  # Gets the username from the form
        password1 = request.form.get('password1')  # Gets the password from the form
        password2 = request.form.get('password2')

        # check if username exists in database
        user = user_collection.find_one({"username": username})
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 2:
            flash('Username too short.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # Add user to database
            new_user = User(username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            user_collection.insert_one(new_user.__to_dict__())
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html")
