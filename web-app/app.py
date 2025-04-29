from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from flask import Flask
from routes.auth_routes import auth_bp, init_auth
from routes.event_routes import event_bp
from routes.profile_routes import profile_bp
from routes.explore_routes import explore_bp
from flask_login import LoginManager, UserMixin, current_user
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback-secret")
app.config["APP_START"] = datetime.now()

# connect to mongo
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client[os.environ.get("MONGO_DBNAME", "test_db")]

login_manager = LoginManager()
login_manager.init_app(app)
app.login_manager = login_manager 
login_manager.login_view = "auth.login"


class User(UserMixin):
    def __init__(self, _id, username, pswdHash, nickname=None, profile_pic=None):
        self.id = str(_id)
        self.username = username
        self.pswdHash = pswdHash
        self.nickname = nickname or username

init_auth(db, User)

# user_loader function
@login_manager.user_loader
def load_user(user_id):
    user_doc = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        return None
    return User(
        _id=user_doc["_id"],
        username=user_doc["username"],
        pswdHash=user_doc["pswdHash"],
        nickname=user_doc.get("nickname", user_doc["username"]),
    )

@app.context_processor
def inject_unread_notifs_count():
    from models import get_notifications_for_user
    if current_user.is_authenticated:
        notifs = get_notifications_for_user(str(current_user.id))
        unread_count = sum(1 for n in notifs if not n.get("seen", False))
    else:
        unread_count = 0
    return dict(unread_notifs_count=unread_count)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(explore_bp)

# so basically this calls all the stuff from the routes files
# this is so that app.py doesnt have a bajillion lines for all the stuff
# instead you can find and edit the files easily within the routes folder 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  