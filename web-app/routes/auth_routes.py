import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId




# creating the blueprint
auth_bp = Blueprint("auth", __name__, template_folder="templates")

_db = None
User = None


def init_auth(db, user_class):
    """Initialize references so we can avoid circular imports"""
    global _db, User
    _db = db
    User = user_class


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # checking for existing user using pymongo
        existingUser = _db.users.find_one({"username": username})
        if existingUser:
            flash("Oops! That username is already taken!")
            return redirect(url_for("auth.signup"))
        pswdHash = generate_password_hash(password)

        result = _db.users.insert_one(
            {
                "username": username,
                "email": email,
                "pswdHash": pswdHash,
                "nickname": username, 
                "profile_pic": "static/nav-icons/profile-icon.svg",
            }
        )
        newId = result.inserted_id

        # User object is created here!
        user = User(
            _id=newId,
            username=username,
            pswdHash=pswdHash,
            nickname=username,  # defaults to username
            profile_pic="static/nav-icons/profile-icon.svg",
            # user_entries=[],
            # user_stats={"total_words": 0, "total_entries": 0}
        )
        login_user(user)
        flash("Account created sucessfully!")
        return redirect(url_for("explore.explore"))

    # flask function to look into the templates folder
    return render_template("auth/signup.html")

'''
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # … authenticate …
        login_user(user)
        session["app_start"] = current_app.config["APP_START"]
        flash("Welcome!")
        return redirect(url_for("explore.explore"))   # ← same redirect
    return render_template("auth/login.html")    
'''  

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Look up the user in the database
        userDoc = _db.users.find_one({"username": username})

        # Check that the user exists and the password matches
        if userDoc and check_password_hash(userDoc["pswdHash"], password):
            # Create a User object
            user = User(
                _id=userDoc["_id"],
                username=userDoc["username"],
                pswdHash=userDoc["pswdHash"],
                nickname=userDoc.get("nickname", userDoc["username"]),
                profile_pic=userDoc.get("profile_pic", "static/nav-icons/profile-icon.svg"),
            )

            login_user(user)
            session["app_start"] = current_app.config["APP_START"]
            flash("Welcome!")
            return redirect(url_for("explore.explore"))  
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("See you next time!")
    return redirect(url_for("auth.login"))