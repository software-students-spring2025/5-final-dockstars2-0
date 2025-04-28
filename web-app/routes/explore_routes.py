from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import get_all_events
explore_bp = Blueprint("explore", __name__, template_folder="templates")

@explore_bp.route("/", methods=["GET"])
@login_required
def explore():
    events = get_all_events()
    return render_template("explore/explore.html", events=events, username=current_user.username)