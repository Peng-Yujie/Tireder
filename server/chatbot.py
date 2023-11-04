from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import emit
from server import socketio
from .models import Chat

chatbot = Blueprint('chatbot', __name__)
# chat = Chat()


@chatbot.route('/chat', methods=['GET', 'POST'])
@login_required
def chat_view():
    return render_template("chatbot.html", user=current_user)


# route for ending: when click on the close button, redirect to home page
# @chatbot.route('/close', methods=['GET', 'POST'])
# @login_required
# def close():
#     if request.method == 'POST':
#         return redirect(url_for('views.home'))
#
#     return render_template('chatbot.html', user=current_user)


chat = Chat()


@socketio.on('message')
def handle_message(msg):
    print(msg)
    print(repr(chat))
    emit('reply_to', chat.get_ai_response(msg['data']), broadcast=False)
