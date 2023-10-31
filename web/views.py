from bson import ObjectId
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import users
from datetime import datetime
from services.utils import get_week_and_day, generate_wall

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # When user submits a form
    if request.method == 'POST':
        # Find user in users and then store the record into the user's records
        add_notes = request.form.get('notes')
        tired_level = request.form.get('tired_level')
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        new_entry = {
            "tired_level": tired_level,
            "add_notes": add_notes,
            "date": date,
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

    # Generate a tiredness wall
    wall = generate_wall(records)

    return render_template("home.html", user=current_user, records=records, wall=wall)
