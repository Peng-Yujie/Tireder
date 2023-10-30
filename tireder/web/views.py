from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import records
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user = current_user.username
        tiredness = request.form.get('tiredness')
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "user": user,
            "tiredness": tiredness,
            "time": time
        }
        records.insert_one(new_entry)

    current_records = list(records.find({"user": current_user.username}))

    return render_template("home.html", user=current_user, records=current_records)
