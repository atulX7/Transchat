from flask import current_app

from app.utils import save_audio_input, PROMPTS


def simulate_conversation(file, lang1, lang2):
    filename = save_audio_input(file)
    print(f"Audio file saved at location: {filename}")
    audio_transcription = current_app.openai.get_audio_transcription(filename)
    print(f"Generated transcription: {audio_transcription}")
    prompt = PROMPTS['conversation'] % (lang1, lang2)
    translated_text = current_app.openai.chat_with_openai(prompt, audio_transcription)
    print(f"translated text: {translated_text}")
    output_file = current_app.openai.generate_translated_audio(translated_text)
    print(f"Got output file at: {output_file}")
    return output_file


def simulate_video_transcription(file, lang, is_source_lang):
    filename = save_audio_input(file)
    print(f"Video file saved at location: {filename}")
    audio_transcription = current_app.openai.get_audio_transcription(filename)
    print(f"Generated transcription: {audio_transcription}")
    transcription = audio_transcription

    if not is_source_lang:
        prompt = PROMPTS['translation'] % (lang)
        transcription = current_app.openai.chat_with_openai(prompt, audio_transcription)
    print(f"transcription: {transcription}")
    return transcription


def simulate_video_conclusion(transcription):
    prompt = PROMPTS['conclude']
    conclusion = current_app.openai.chat_with_openai(prompt, transcription)
    print(f"conclusion: {conclusion}")
    return conclusion