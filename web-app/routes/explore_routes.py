from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import get_all_events, get_event_by_id

explore_bp = Blueprint("explore", __name__, template_folder="templates")

#DISPLAAYYY EVENNTTTTTS
@explore_bp.route("/", methods=["GET"])
@login_required
def explore():
    events = get_all_events()
    return render_template("explore/explore.html", events=events, username=current_user.username)


#GET EVENT DETAIILLLL
@explore_bp.route("/event/<event_id>")
@login_required
def event_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash("Event not found.")
        return redirect(url_for("explore.explore"))
    return render_template("event/event_detail.html", event=event)

#SEAARRRCCHHHHH!
@explore_bp.route("/search", methods=["GET"])
@login_required
def search_events():
    query = request.args.get("query", "").lower()
    events = get_all_events()
    filtered_events = [event for event in events if query in event["title"].lower()]
    
    # only one match, go to its event detail page
    if len(filtered_events) == 1:
        return redirect(url_for("explore.event_detail", event_id=filtered_events[0]["id"]))
    
    return render_template(
        "explore/explore.html",
        events=filtered_events,
        username=current_user.username
    )
