from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from models import (
    get_event_by_id,
    get_user_folders,
    get_user_by_id,
    db,
    fs
)
from werkzeug.security import generate_password_hash

profile_bp = Blueprint("profile", __name__, template_folder="templates/profile")

@profile_bp.route("/profile")
@login_required
def profile():
    user_data = get_user_by_id(current_user.id)
    if not user_data:
        flash("User not found.")
        return redirect(url_for('auth.login'))

    folders = get_user_folders(str(current_user.id))

    def fetch_events(key):
        ids = db.users.find_one({"_id": ObjectId(current_user.id)}).get(key, [])
        return [get_event_by_id(eid) for eid in ids if get_event_by_id(eid)]

    return render_template(
        "profile/profile.html",
        user=user_data,
        folders=folders,
        created_events=fetch_events("created_events"),
        planning_events=fetch_events("planning_events"),
        maybe_events=fetch_events("maybe_events"),
        attended_events=fetch_events("attended_events")
    )

@profile_bp.route("/create-board", methods=["GET", "POST"])
@login_required
def create_board():
    if request.method == "POST":
        board_name = request.form.get("name", "").strip()
        if not board_name:
            flash("Board name cannot be empty.")
            return redirect(url_for("profile.create_board"))

        db.folders.insert_one({
            "user_id": str(current_user.id),
            "name": board_name,
            "event_ids": []
        })
        flash("Board created successfully!")
        return redirect(url_for("profile.profile"))

    return render_template("profile/create_board.html")

@profile_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        new_pic_file = request.files.get("profile_image")
        new_pic_url = request.form.get("profile_pic")

        updates = {}

        if new_username:
            updates["username"] = new_username

        if new_password:
            updates["pswdHash"] = generate_password_hash(new_password)

        if new_pic_file and new_pic_file.filename != '':
            filename = secure_filename(new_pic_file.filename)
            image_id = fs.put(new_pic_file, filename=filename)
            updates["profile_pic_id"] = image_id
            updates.pop("profile_pic", None)
        elif new_pic_url:
            updates["profile_pic"] = new_pic_url
            updates.pop("profile_pic_id", None)

        if updates:
            db.users.update_one(
                {"_id": ObjectId(current_user.id)},
                {"$set": updates}
            )
            flash("Settings updated successfully!", "success")
            return redirect(url_for("profile.profile"))
        else:
            flash("No changes submitted.", "info")

    return render_template("profile/settings.html", user=get_user_by_id(current_user.id))
