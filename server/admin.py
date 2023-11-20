from flask import Blueprint, render_template
from flask_login import login_required, current_user
from server import users

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
def dashboard():
    print(current_user.admin)
    if current_user.admin:
        # get all users from the database
        users_json = users.find({})
        return render_template('admin.html', user=current_user, users=users_json)
    else:
        print("not admin")
        return render_template('home.html', user=current_user)
