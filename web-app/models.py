import os
from dotenv import load_dotenv
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

load_dotenv()

# connect to mongo
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client[os.environ.get("MONGO_DBNAME", "yonder")]
fs = gridfs.GridFS(db)

def get_event_by_id(event_id):
    data = db.events.find_one({"_id": ObjectId(event_id)})
    if not data:
        return None
    return {
        "id": str(data["_id"]),
        "title": data["title"],
        "description": data["description"],
        "image_id": str(data["image_id"]),
        "date": data["date"],
        "location": data["location"],
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "creator_username": data.get("creator_username", "Unknown")
    }


def get_comments_for_event(event_id):
    comments = db.comments.find({"event_id": event_id})
    return [{"username": c["username"], "text": c["text"]} for c in comments]


def get_user_folders(user_id):
    folders = db.folders.find({"user_id": user_id})
    return [{"id": str(f["_id"]), "name": f["name"]} for f in folders]


def save_event_to_folder(user_id, event_id, folder_id):
    db.folders.update_one(
        {"_id": ObjectId(folder_id), "user_id": user_id},
        {"$addToSet": {"event_ids": event_id}}
    )


def add_comment_to_event(user_id, event_id, text):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    username = user["username"] if user else "Unknown"
    db.comments.insert_one({
        "event_id": event_id,
        "user_id": user_id,
        "username": username,
        "text": text
    })


def create_event(user_id, title, description, image_id, date, location, latitude=None, longitude=None):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    username = user["username"] if user else "Unknown"

    event_data = {
        "title": title,
        "description": description,
        "image_id": image_id,
        "date": date,
        "location": location,
        "creator_id": user_id,
        "creator_username": username
    }

    if latitude and longitude:
        event_data["latitude"] = float(latitude)
        event_data["longitude"] = float(longitude)

    result = db.events.insert_one(event_data)
    return result.inserted_id


def get_all_events():
    events = []
    for doc in db.events.find({}):
        events.append({
            "id": str(doc["_id"]),
            "title": doc.get("title"),
            "description": doc.get("description"),
            "image_id": str(doc.get("image_id")),
            "date": doc.get("date"),
            "location": doc.get("location"),
            "latitude": doc.get("latitude"),
            "longitude": doc.get("longitude"),
            "creator_username": doc.get("creator_username", "Unknown")
        })
    return events


def delete_event_by_id(event_id):
    db.events.delete_one({"_id": ObjectId(event_id)})


def update_event_by_id(event_id, title, description, image_id, date, location, latitude=None, longitude=None):
    update_fields = {
        "title": title,
        "description": description,
        "image_id": image_id,
        "date": date,
        "location": location
    }
    if latitude and longitude:
        update_fields["latitude"] = float(latitude)
        update_fields["longitude"] = float(longitude)

    db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": update_fields}
    )


def get_user_by_id(user_id):
    """Return a user dict with profile pic info"""
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "username": user.get("username", "Unknown"),
        "profile_pic_url": user.get("profile_pic"),
        "profile_pic_id": str(user["profile_pic_id"]) if user.get("profile_pic_id") else None
    }
