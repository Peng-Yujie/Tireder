from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from server import users
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def dashboard():
    print(current_user.admin)
    if current_user.admin:
        # get all users from the database
        users_data = users.find({})
        users_num = users.count_documents({})
        records_num = 0
        bricks_num = 0
        for user in users.find():
            records_num += len(user.get("records", []))
            bricks_num += len(user.get("bricks", {}))
        return render_template('admin/admin.html',
                               user=current_user,
                               users=users_data,
                               users_num=users_num,
                               records_num=records_num,
                               bricks_num=bricks_num)
    else:
        print("not admin")
        return render_template('home.html', user=current_user)


@admin.route('/delete/<username>', methods=['POST'])
@login_required
def delete_user(username):
    try:
        users.delete_one({"username": username})
        flash('User deleted!', category='success')
    except:
        flash('Error!', category='error')

    return redirect(url_for('admin.dashboard'))


@admin.route('/add', methods=['POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check if username exists in database
        new_user = users.find_one({"username": username})
        if new_user:
            flash('Username already exists.', category='error')
        elif len(username) < 2:
            flash('Username too short.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # Add new user to database
            user_json = {
                "username": username,
                "password": generate_password_hash(password, method='pbkdf2:sha256'),
                "records": [],
                "bricks": {}
            }
            users.insert_one(user_json)
            flash('Account created!', category='success')
    return redirect(url_for('admin.dashboard'))


@admin.route('/details/<username>', methods=['GET'])
@login_required
def details(username):
    try:
        # get user from the database
        user_json = users.find_one({"username": username})
        if user_json:
            records = user_json.get("records", [])
            return render_template('admin/details.html', user=current_user, records=records, username=username)
    except:
        flash('Error!', category='error')
        return redirect(url_for('admin.dashboard'))

    return redirect(url_for('admin.dashboard'))
