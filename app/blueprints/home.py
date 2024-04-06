from flask import Blueprint, jsonify, render_template, send_from_directory, current_app

# from flask_login import current_user

blueprint = Blueprint("home", __name__)


@blueprint.get("/chat")
def converse_index():
    # if current_user.is_authenticated:
    #     name = current_user.firstname
        # return render_template(
        #     "home/index.html",
        # )
    return render_template('converse_index.html')


@blueprint.get("/transcribe")
def video_transcriber_index():
    return render_template('transcribe_index.html')


@blueprint.get("/liveness")
def liveness():
    return "Alive"
