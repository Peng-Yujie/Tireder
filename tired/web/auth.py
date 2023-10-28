from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html", text="text")
    # TODO: text="text" is a variable that can be used in the html file
    # we can use this to pass in a variable to the html file


@auth.route('/logout')
def logout():
    return render_template("logout.html")


@auth.route('/signup')
def signup():
    return render_template("signup.html")
