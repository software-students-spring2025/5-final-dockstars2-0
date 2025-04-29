from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from models import (
    get_event_by_id,
    get_user_folders,
    save_event_to_folder,
    create_event, 
    delete_event_by_id,
    update_event_by_id,
    db,
    fs
)
import io
from werkzeug.utils import secure_filename

event_bp = Blueprint("event", __name__, template_folder="event")


@event_bp.route("/event/<event_id>/signup", methods=["POST"])
@login_required
def signup_event(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash("Event not found.")
        return redirect(url_for("explore.explore"))

    selected_board = request.form.get("board")

    if selected_board == "new":
        # USER PICKED "NEW"
        board_name = f"{event['title']} Board"  # default name or later make it custom
        new_folder = db.folders.insert_one({
            "user_id": str(current_user.id),
            "name": board_name,
            "event_ids": [ObjectId(event_id)]
        })

        # after creating, redirect to view that new board
        new_board_id = str(new_folder.inserted_id)
        flash("Board created and event saved!")
        return redirect(url_for("profile.view_board", board_id=new_board_id))

    else:
        # Save to existing folder
        save_event_to_folder(str(current_user.id), event_id, selected_board)

        # create notif if saving on someone else's event
        if str(current_user.id) != event["creator_id"]:
            from models import add_notification
            add_notification(
                user_id=event["creator_id"],
                type="save",
                event_id=event_id,
                message=f"{current_user.username} saved your event '{event['title']}'"
            )

        flash("Saved successfully!")
        return redirect(url_for("explore.event_detail", event_id=event_id))






@event_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        # handle image file
        image_file = request.files.get("image")
        image_id = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_id = fs.put(image_file, filename=filename)

        event_id = create_event(
            user_id=str(current_user.id),
            title=title,
            description=description,
            image_id=image_id,
            date=date,
            location=location,
            latitude=latitude,
            longitude=longitude
        )

        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$push": {"created_events": ObjectId(event_id)}}
        )

        flash("Event created successfully!")
        return redirect(url_for("explore.explore"))

    return render_template("event/add_event.html")



@event_bp.route("/event/<event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    delete_event_by_id(event_id)
    flash("Event deleted successfully!")
    return redirect(url_for("explore.explore"))


@event_bp.route("/event/<event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash("Event not found.")
        return redirect(url_for("explore.explore"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")

        image_file = request.files.get("image")
        image_id = event["image_id"]  # default to existing
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_id = fs.put(image_file, filename=filename)

        update_event_by_id(
        event_id,
        title=title,
        description=description,
        image_id=event["image_id"],  # keep existing
        date=date,
        location=event["location"]   # keep existing
        )

        flash("Event updated successfully!")
        return redirect(url_for("explore.event_detail", event_id=event_id))

    return render_template("edit_event.html", event=event)


@event_bp.route("/event/<event_id>/plan", methods=["POST"])
@login_required
def plan_to_attend(event_id):
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"planning_events": ObjectId(event_id)}}
    )
    flash("You're planning to attend this event!")
    return redirect(url_for("profile.profile"))


@event_bp.route("/event/<event_id>/maybe", methods=["POST"])
@login_required
def maybe_attend(event_id):
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"maybe_events": ObjectId(event_id)}}
    )
    flash("You've marked this as maybe attending.")
    return redirect(url_for("profile.profile"))

# serve images
@event_bp.route("/image/<image_id>")
def get_image(image_id):
    try:
        file = fs.get(ObjectId(image_id))
        return send_file(io.BytesIO(file.read()), mimetype="image/jpeg")
    except Exception:
        return "Image not found", 404

@event_bp.route("/event/<event_id>/comment", methods=["POST"])
@login_required
def add_comment(event_id):
    comment_text = request.form.get("comment_text")
    if comment_text:
        event = get_event_by_id(event_id)
        db.comments.insert_one({
            "event_id": event_id,
            "user_id": str(current_user.id),
            "username": current_user.username,
            "text": comment_text
        })

        # create notification
        if str(current_user.id) != event["creator_id"]:
            from models import add_notification
            add_notification(
                user_id=event["creator_id"],
                type="comment",
                event_id=event_id,
                message=f"{current_user.username} commented on your event '{event['title']}'"
            )

    return redirect(url_for("explore.event_detail", event_id=event_id))
