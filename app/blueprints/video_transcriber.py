from flask import Flask, request, jsonify, Blueprint

from app.services import simulate_video_conclusion, simulate_video_transcription

blueprint = Blueprint("video_transcriber", __name__)


@blueprint.route('/transcribe', methods=['POST'])
def transcribe_video():
    video_file = request.files['video']
    language = request.form['language']
    is_source_lang = True
    transcript = simulate_video_transcription(video_file, language, is_source_lang)
    return jsonify({'transcript': transcript})


@blueprint.route('/conclude', methods=['POST'])
def conclude_video():
    video_file = request.files['video']
    language = request.form['language']
    is_source_lang = True
    transcript = simulate_video_transcription(video_file, language, is_source_lang)
    conclusion = simulate_video_conclusion(transcript)
    return jsonify({'transcript': conclusion})
