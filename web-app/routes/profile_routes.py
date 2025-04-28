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
    folders = get_user_folders(str(current_user.id))

    # Load events the user is planning or maybe attending (COMBINED)
    planning_event_ids = getattr(current_user, "planning_events", []) + getattr(current_user, "maybe_events", [])
    planning_events = []
    for event_id in planning_event_ids:
        event = get_event_by_id(event_id)
        if event:
            planning_events.append(event)

    # Load events the user has attended
    attended_event_ids = getattr(current_user, "attended_events", [])
    attended_events = []
    for event_id in attended_event_ids:
        event = get_event_by_id(event_id)
        if event:
            attended_events.append(event)

    return render_template("profile/profile.html", 
                           user=current_user,
                           folders=folders,
                           planning_events=planning_events,
                           attended_events=attended_events)

@profile_bp.route("/create-board", methods=["GET", "POST"])
@login_required
def create_board():
    if request.method == "POST":
        board_name = request.form.get("board_name")
        if not board_name:
            flash("Board name cannot be empty.")
            return redirect(url_for("profile.create_board"))

        _db.folders.insert_one({
            "user_id": str(current_user.id),
            "name": board_name,
            "event_ids": []
        })
        flash("Board created successfully!")
        return redirect(url_for("profile.profile"))

    return render_template("profile/create_board.html")