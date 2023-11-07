from bson import ObjectId
from flask import Blueprint, render_template, request,redirect, url_for
from flask_login import login_required, current_user
from server import users
from datetime import datetime
from server.models import Brick, Wall

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # When user submits a form
    if request.method == 'POST':
        # Find user in users and then store the record into the user's records
        add_notes = request.form.get('add_notes')
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
        update_result = users.update_one(
            {"_id": ObjectId(current_user.get_id())},
            {"$push": {"records": new_entry}}
        )
        # Update the user's bricks
        if update_result.modified_count > 0:
            user = users.find_one({"_id": ObjectId(current_user.get_id())})
            bricks = user.get("bricks", {})
            # print(bricks)
            if date in bricks:
                brick = Brick.from_json(bricks[date])
                brick.update(tired_level)
                bricks[date] = brick.to_json()
            else:
                new_brick = Brick(1, int(tired_level))
                bricks[date] = new_brick.to_json()

            # Update the user's bricks
            users.update_one(
                {"_id": ObjectId(current_user.get_id())},
                {"$set": {"bricks": bricks}}
            )
        return redirect(url_for('views.home'))

    # Get the user's records
    user = users.find_one({"_id": ObjectId(current_user.get_id())})
    records = user.get("records", [])
    bricks = user.get("bricks", {})
    today = datetime.now().strftime("%Y-%m-%d")

    # Generate a tiredness wall
    wall = Wall(bricks).wall_list

    return render_template('home.html', user=current_user, records=records, wall=wall, today=today)


@views.route('/chat')
@login_required
def chat():
    user_id = current_user.get_id()
    user_name = users.find_one({"_id": ObjectId(user_id)}).get("username", "My friend")
    return render_template("chatbot.html", user=current_user, name=user_name)
