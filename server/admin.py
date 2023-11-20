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
        users_data = users.find({})
        users_num = users.count_documents({})
        records_num = 0
        bricks_num = 0
        for user in users.find():
            records_num += len(user.get("records", []))
            bricks_num += len(user.get("bricks", {}))
        return render_template('admin.html',
                               user=current_user,
                               users=users_data,
                               users_num=users_num,
                               records_num=records_num,
                               bricks_num=bricks_num)
    else:
        print("not admin")
        return render_template('home.html', user=current_user)

