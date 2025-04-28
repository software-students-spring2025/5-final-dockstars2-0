from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from models import (
    get_event_by_id,
    get_user_folders,
    save_event_to_folder,
    create_event, 
    delete_event_by_id,
    update_event_by_id
)
from models import db



event_bp = Blueprint("event", __name__, template_folder="templates/event")

@event_bp.route("/event/<event_id>/signup", methods=["GET", "POST"])
@login_required
def signup_event(event_id):
    if "user_id" not in session:
        flash("You must be logged in to sign up for events.")
        return redirect(url_for("auth.login"))

    event = get_event_by_id(event_id)
    folders = get_user_folders(session["user_id"])

    if request.method == "POST":
        selected_folder = request.form.get("folder")
        if selected_folder == "new":
            return redirect(url_for('profile.create_board'))

        save_event_to_folder(session["user_id"], event_id, selected_folder)
        flash("Event saved successfully!")
        return redirect(url_for("profile.profile"))

    return render_template("event_signup.html", event=event, folders=folders)

@event_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        date = request.form.get("date")
        location = request.form.get("location")
        
        event_id = create_event(
            user_id=str(current_user.id),
            title=title,
            description=description,
            image_url=image_url,
            date=date,
            location=location
        )

        db.users.update_one(
            {"_id": ObjectId(current_user._id)},
            {"$push": {"created_events": ObjectId(event_id)}}
        )

        flash("Event created successfully!")
        return redirect(url_for("auth.explore"))

    return render_template("create_event.html")

@event_bp.route("/event/<event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    delete_event_by_id(event_id)
    flash("Event deleted successfully!")
    return redirect(url_for("auth.explore"))

@event_bp.route("/event/<event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash("Event not found.")
        return redirect(url_for("auth.explore"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        date = request.form.get("date")
        location = request.form.get("location")

        update_event_by_id(event_id, title, description, image_url, date, location)

        flash("Event updated successfully!")
        return redirect(url_for("auth.explore"))

    return render_template("edit_event.html", event=event)

@event_bp.route("/event/<event_id>/plan", methods=["POST"])
@login_required
def plan_to_attend(event_id):
    db.users.update_one(
        {"_id": ObjectId(current_user._id)},
        {"$addToSet": {"planning_events": ObjectId(event_id)}}
    )
    flash("You are now planning to attend this event!")
    return redirect(url_for("profile.profile"))

@event_bp.route("/event/<event_id>/maybe", methods=["POST"])
@login_required
def maybe_attend(event_id):
    db.users.update_one(
        {"_id": ObjectId(current_user._id)},
        {"$addToSet": {"maybe_events": ObjectId(event_id)}}
    )
    flash("You've marked this event as maybe attending.")
    return redirect(url_for("profile.profile"))






