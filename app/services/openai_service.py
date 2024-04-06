import os
import time

from flask import current_app
from openai import OpenAI

from app.utils import remove_file


class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.model_name= "gpt-4-0125-preview"

    def chat_with_openai(self, prompt, input):
        """
        Sends the prompt to OpenAI API using the chat interface and gets the model's response.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": input
                }
            ],
            temperature=0.7,
            max_tokens=64,
            top_p=1
        )
        chatbot_response = response.choices[0].message.content
        return chatbot_response.strip()

    def get_audio_transcription(self, audio_filename):
        audio_transcription = ''
        try:
            audio_file_obj = open(audio_filename, "rb")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file_obj,
                response_format="text"
            )
            audio_transcription = transcription
        except Exception as e:
            print(f"Failed to translate audio due to: {e}")
        return audio_transcription


    def generate_translated_audio(self, translated_text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=translated_text,
        )
        output_file = os.path.join(current_app.config['OUTPUT_FOLDER'], "output.mp3")
        remove_file(output_file)
        response.stream_to_file(output_file)
        return output_file

