import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

# connect to mongo
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client[os.environ.get("MONGO_DBNAME")]

def get_event_by_id(event_id):
    # MongoDB find event by ID
    data = db.events.find_one({"_id": ObjectId(event_id)})
    if not data:
        return None
    return {
        "id": str(data["_id"]),
        "title": data["title"],
        "description": data["description"],
        "image_url": data["image_url"],
        "date": data["date"],
        "location": data["location"],
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
'''
def create_event(user_id, title, description, image_url, date, location):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    username = user["username"] if user else "Unknown"
    db.events.insert_one({
        "title": title,
        "description": description,
        "image_url": image_url,
        "date": date,
        "location": location,
        "creator_id": user_id,
        "creator_username": username
    })
'''
def create_event(user_id, title, description, image_url, date, location):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    username = user["username"] if user else "Unknown"

    result = db.events.insert_one({
        "title": title,
        "description": description,
        "image_url": image_url,
        "date": date,
        "location": location,
        "creator_id": user_id,
        "creator_username": username
    })

    return result.inserted_id   



def get_all_events():
    events = []
    for doc in db.events.find({}):
        events.append({
            "id": str(doc["_id"]),
            "title": doc.get("title"),
            "description": doc.get("description"),
            "image_url": doc.get("image_url"),
            "date": doc.get("date"),
            "location": doc.get("location"),
            "creator_username": doc.get("creator_username", "Unknown")
        })
    return events

def delete_event_by_id(event_id):
    db.events.delete_one({"_id": ObjectId(event_id)})

def update_event_by_id(event_id, title, description, image_url, date, location):
    db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {
            "title": title,
            "description": description,
            "image_url": image_url,
            "date": date,
            "location": location
        }}
    )