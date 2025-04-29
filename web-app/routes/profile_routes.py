from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import get_user_folders, get_event_by_id
from bson.objectid import ObjectId
from models import db



profile_bp = Blueprint("profile", __name__, template_folder="templates/profile")

@profile_bp.route("/profile")
@login_required
def profile():
    # Load user folders

    user_doc = db.users.find_one({"_id": ObjectId(current_user.id)})

    if not user_doc:
        flash("User not found.")
        return redirect(url_for('auth.login'))

    folders = get_user_folders(str(current_user.id))

    created_events = []
    for event_id in user_doc.get("created_events", []):
        event = get_event_by_id(event_id)
        if event:
            created_events.append(event)

    planning_events = []
    for event_id in user_doc.get("planning_events", []):
        event = get_event_by_id(event_id)
        if event:
            planning_events.append(event)

    maybe_events = []
    for event_id in user_doc.get("maybe_events", []):
        event = get_event_by_id(event_id)
        if event:
            maybe_events.append(event)

    attended_events = []
    for event_id in user_doc.get("attended_events", []):
        event = get_event_by_id(event_id)
        if event:
            attended_events.append(event)

    return render_template(
        "profile/profile.html",
        user=current_user,
        folders=folders,
        created_events=created_events,
        planning_events=planning_events,
        maybe_events=maybe_events,
        attended_events=attended_events
    )

@profile_bp.route("/create-board", methods=["GET", "POST"])
@login_required
def create_board():
    if request.method == "POST":
        board_name = request.form.get("board_name")
        if not board_name.strip():
            flash("Board name cannot be empty.")
            return redirect(url_for("profile.create_board"))

        db.folders.insert_one({
            "user_id": str(current_user.id),
            "name": board_name.strip(),
            "event_ids": []
        })
        flash("Board created successfully!")
        return redirect(url_for("profile.profile"))

    return render_template("profile/create_board.html")
