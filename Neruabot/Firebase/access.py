import firebase_admin
import json
from firebase_admin import db


class Access():
    def __init__(self, students_or_teachers="teachers"):
        cred = firebase_admin.credentials.Certificate(
            'Neruabot/Firebase/neuracode-discord-bot-firebase-adminsdk-mor5r-5576ccdbbf.json')
        self.default_app = firebase_admin.initialize_app(cred, {
            "databaseURL": "https://neuracode-discord-bot-default-rtdb.firebaseio.com/"})


    def set_data(self):
        ref = db.reference("/")
        with open("data.json", "r") as f:
            file_contents = json.load(f)
        ref.set(file_contents)

    def view_all_hours(self, collection_name):
        ref = db.reference(f"/{collection_name}")
        return ref.get()

    def read_hours(self, collection_name, document_id):
        # returns only one user's hours
        # collection name is the students or teachers in data.json
        # document id is the user id discord gives them on discord
        ref = db.reference(f"/{collection_name}/{document_id}")
        return ref, ref.get()

    def add_hours(self, collection_name, document_id, hours):
        user, user_info = self.read_hours(collection_name, document_id)
        if user_info is not None:
            user.update({
                'hours': user_info['hours'] + hours
            })
        else:
            user.set({
                'hours': hours
            })
    def remove_hours(self, collection_name, document_id, hours):
        user, user_info = self.read_hours(collection_name, document_id)
        if user_info is not None:
            num = user_info['hours'] - hours
            if num < 0:
                num = 0
            user.update({
                'hours': num
            })
        else:
            user.set({
                'hours': 0
            })

