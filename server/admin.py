from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin_dashboard():
    print(current_user.admin)
    if current_user.admin:
        return render_template('admin.html')
    else:
        return render_template('home.html', user=current_user)
