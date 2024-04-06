import logging
import os
import re

from flask import current_app


def save_audio_input(audio):
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], audio.filename)
    remove_file(filename)
    audio.save(filename)
    return filename


def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
