from flask import Flask
from routes.auth_routes import auth_bp
from routes.event_routes import event_bp
from routes.profile_routes import profile_bp
from routes.explore_routes import explore_bp

app = Flask(__name__)
app.secret_key = "supersecret" # change later w env

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(explore_bp)

# so basically this calls all the stuff from the routes files
# this is so that app.py doesnt have a bajillion lines for all the stuff
# instead you can find and edit the files easily within the routes folder 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
