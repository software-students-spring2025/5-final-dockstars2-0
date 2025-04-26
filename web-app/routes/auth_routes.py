import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
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

        # checking for existing user using pymongo
        existingUser = _db.users.find_one({"username": username})
        if existingUser:
            # flash - stores one-time msg int he user's session to display it on the next page load
            flash("Oops! That username is already taken!")
            return redirect(url_for("auth.signup"))
        # Note: passwords need to be hashed! 
        # WARNING: Fails on certain computers!
        #pswdHash = generate_password_hash(password)
        #pswdHash = password
        pswdHash = generate_password_hash(password)

        result = _db.users.insert_one({
            "username": username, 
            "pswdHash": pswdHash,
            "nickname": username, #username by default
            "profile_pic": "static/nav-icons/profile-icon.svg",
            #"user_stats":{
                #"total_words": 0,
                #"total_entries": 0
            },
            #"user_entries": []
           # })
        newId = result.inserted_id

        # User object is created here!
        user = User(
            _id=newId, 
            username=username, 
            pswdHash = pswdHash,
            nickname=username,  # defaults to username
            profile_pic="static/nav-icons/profile-icon.svg",
            #user_entries=[],
            #user_stats={"total_words": 0, "total_entries": 0}
        )
        login_user(user)
        flash("Account created sucessfully!")
        return redirect(url_for("auth.dashboard"))
    
    # flask function to look into the templates folder
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])