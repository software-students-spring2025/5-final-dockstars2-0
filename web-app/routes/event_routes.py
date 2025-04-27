from flask import session, redirect, url_for, flash

@app.route("/event/<event_id>/signup", methods=["GET", "POST"])
def signup_event(event_id):
    if "user_id" not in session:
        flash("You must be logged in to sign up for events.")
        return redirect(url_for("auth.login"))

    # Fetch event info, user's collections/folders, etc.
    event = get_event_by_id(event_id)
    folders = get_user_folders(session["user_id"])

    if request.method == "POST":
        selected_folder = request.form.get("folder")
        if selected_folder == "new":
            return redirect(url_for('profile.create_board'))

        # handle saving to selected folder
        save_event_to_folder(session["user_id"], event_id, selected_folder)
        flash("Event saved successfully!")
        return redirect(url_for("profile.profile"))

    return render_template("event_signup.html", event=event, folders=folders)
