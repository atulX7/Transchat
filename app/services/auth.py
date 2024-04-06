from flask import session
from flask_login import login_user, logout_user
from app.mixin import User


def _session_login(sender, subject, attributes, auth):
    first_name = attributes.get("FirstName")[0]
    last_name = attributes.get("LastName")[0]
    email = attributes.get("Email")[0]
    groups = attributes.get("Groups")
    user = User(email, first_name, last_name, groups)
    login_user(user)
    session.permanent = True
    session["user_info"] = {
        "firstname": first_name,
        "lastname": last_name,
        "email": email,
        "groups": groups,
    }


def _session_logout(sender):
    session.clear()
    logout_user()
