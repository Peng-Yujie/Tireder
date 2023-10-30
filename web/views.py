from bson import ObjectId
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import users
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # When user submits a form
    if request.method == 'POST':
        # Find user in users and then store the record into the user's records
        tiredlevel = request.form.get('tiredlevel')
        notes = request.form.get('notes')
        # tiredness = request.form.get('tiredness')
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            # "tiredness": tiredness,
            "tiredlevel": tiredlevel,
            "notes": notes,
            "time": time
        }
        # Update the user's records
        users.update_one(
            {"_id": ObjectId(current_user.get_id())},
            {"$push": {"records": new_entry}}
        )

    # Get the user's records
    user = users.find_one({"_id": ObjectId(current_user.get_id())})
    records = user["records"]

    return render_template("home.html", user=current_user, records=records)
