import pyrebase
import json
import uuid

class DBModule:
    def __init__(self):
        with open("./auth/auth.json") as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def register_verification(self, id_):
        users = self.db.child("users").get().val()
        for user_id in users.keys():
            if id_ == user_id:
                return False
        return True

    def register(self, id_, password, name, email):
        user_data = { 
            "user_password": password,
            "user_name": name,
            "user_email": email
        }
        if self.register_verification(id_):
            self.db.child("users").child(id_).set(user_data)
            return True
        else:
            return False
        
    def login_verification(self, id_, password):
        users = self.db.child("users").get().val()
        try:
            if users[id_]:
                if password == users[id_]["user_password"]:
                    return 1
                else:
                    return 0
        except:
            return -1
    
    def get_userdata(self, id_):
        users = self.db.child("users").get().val()
        return users[id_]

    def write(self, id_, title, contents, write_time):
        post_id = uuid.uuid4()
        u_data = self.get_userdata(id_)
        post_data = {
            "title": title,
            "contents": contents,
            "write_time": write_time,
            "user_name": u_data["user_name"],
            "user_id": id_
        }
        self.db.child("posts").child(post_id).set(post_data)

    def get_postdata(self):
        return self.db.child("posts").get().val()
    
    def get_post_detail(self, post_id):
        return self.db.child("posts").get().val()[post_id]
