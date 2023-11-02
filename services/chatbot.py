from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

chatbot = Blueprint('chatbot', __name__)


@chatbot.route('/chat', methods=['GET', 'POST'])
@login_required
def chatbot():
    name = current_user.user_json['name']

    return render_template("chatbot.html", user=current_user, name=name)


# route for ending: when click on the close button, redirect to home page
@chatbot.route('/close', methods=['GET', 'POST'])
@login_required
def close():
    if request.method == 'POST':
        return redirect(url_for('views.home'))

    return render_template("chatbot.html", user=current_user)
