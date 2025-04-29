from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import get_notifications_for_user, mark_notification_seen

notifications_bp = Blueprint("notifications", __name__, template_folder="templates/notifications")

@notifications_bp.route("/notifications")
@login_required
def notifications():
    notifs = get_notifications_for_user(str(current_user.id))
    return render_template("notifications/notifications.html", notifs=notifs)

@notifications_bp.route("/notifications/seen/<notif_id>", methods=["POST"])
@login_required
def mark_seen(notif_id):
    mark_notification_seen(notif_id)
    return redirect(url_for("notifications.notifications"))
