
from flask import request, jsonify, send_from_directory,  Blueprint, current_app
import os

from app.services import simulate_conversation

blueprint = Blueprint("converse", __name__)


@blueprint.route('/conversation', methods=['POST'])
def converse():
    file = request.files['file']
    lang1 = request.form['lang1']
    lang2 = request.form['lang2']
    print(f"start conversating between languages: {lang1} and {lang2}")

    translated_file = simulate_conversation(file, lang1, lang2)
    return jsonify({'filePath': translated_file})


@blueprint.route('/output/<filename>', methods=['GET'])
def output_file(filename):
    output_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'output'))
    return send_from_directory(output_folder, filename)
