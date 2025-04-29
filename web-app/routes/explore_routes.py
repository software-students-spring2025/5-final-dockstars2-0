from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import get_all_events, get_event_by_id, get_user_folders
import random

explore_bp = Blueprint("explore", __name__, template_folder="templates")


@explore_bp.route("/", methods=["GET"])
def explore():
    events = get_all_events()
    # Randomize the event order for a true "explore" vibe
    events = [e for e in events if e is not None]
    random.shuffle(events)

    if current_user.is_authenticated:
        return render_template("explore/explore.html", events=events, username=current_user.username)
    else:
        return render_template("explore/landing.html")


@explore_bp.route("/home", methods=["GET"])
def explore_home():
    events = get_all_events()
    events = [e for e in events if e is not None]
    random.shuffle(events)

    if current_user.is_authenticated:
        return render_template("explore/explore.html", events=events, username=current_user.username)
    else:
        return render_template("explore/explore.html", events=events, username=None)


@explore_bp.route("/event/<event_id>")
def event_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash("Event not found.")
        return redirect(url_for("explore.explore"))

    from models import get_comments_for_event
    comments = get_comments_for_event(event_id)

    folders = get_user_folders(str(current_user.id))

    return render_template(
        "event/event_detail.html",
        event=event,
        comments=comments,
        folders=folders
    )



@explore_bp.route("/search", methods=["GET"])
def search_events():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return redirect(url_for("explore.explore"))  # if no search term, just go back

    events = get_all_events()
    events = [e for e in events if e is not None]

    # search across title, description, location
    filtered_events = []
    for event in events:
        if (
            query in event.get("title", "").lower()
            or query in event.get("description", "").lower()
            or query in event.get("location", "").lower()
        ):
            filtered_events.append(event)

    return render_template(
        "explore/explore.html",
        events=filtered_events,
        username=current_user.username,
        query=query  # pass the search query so the template knows it's a search
    )

