from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, first_name, last_name, groups):
        self.id = user_id
        self.firstname = first_name
        self.lastname = last_name
        self.groups = groups
