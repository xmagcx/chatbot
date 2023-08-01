"""
Storyteller: A simple audio storytelling app using OpenAI API.

Example Usage:
    python anexo.py --address=127.0.0.1 --port=7860
"""

import base64
#import config
import gradio as gr
import io
import os
from typing import Dict, List, Tuple
from bard import Bard
from transcribe import Transcribe 
from speach import Speach 

URL_BARD = "http://localhost:8080/ask"
COOKIE_BARD = "ZAirF-Ur-UgrJjsy7JQtpdycxIvG1pX_KucTypvPp5dXMPbNggOBBbO_x6MREM5OXUJ4kQ."
URL_SPEACH_TEXT = "http://localhost:8081/uploadfile/"
LANG_SPEACH_TEXT = "es-ES"
URL_TEXT_SPEACH  = "http://localhost:8082/audio"
GENERATED_SPEECH_PATH = "generated_speech.mp3"

def text_speach(url,context):
    model = Speach(url,context)
    response = model.request()
    print(response)
    result = ""
    if response.status_code == 200:
        result = response.text
    else:
        result = "Hay un problema con mi Modelo"
    return result

def generate_response(prompt_input,idbard):
    normalized=""
    
    model = Bard(URL_BARD,idbard,prompt_input)
    response = model.request()
    print(response)
    
    if response.status_code == 200:
        normalized = clean_text(response.text)
        print(normalized)
    else:
        normalized = "Hay un problema con mi Modelo"
    return normalized

def speach_text(url,file,lang):
    model = Transcribe(url,file,lang)
    response = model.request()
    print(response)
    result = ""
    if response.status_code == 200:
        result = response.text
    else:
        result = "Hay un problema con mi Modelo"
    return result

def clean_text (text):
    text = text.replace("\\n", " ").replace('"',"").replace("*","")
    return text


# Initial message
messages = [
    {
        "role": "system",
        "content": "Chat de pruebas para utilizar Bard API",
    }
]


"""
Main functions
"""


def transcribe_audio(audio_file: str) -> str:
    """
    Transcribe audio file using API.

    Args:
        audio: stringified path to audio file. WAV file type.

    Returns:
        str: Transcription of audio file
    """
    # gradio sends in a .wav file type, but it may not be named that. Rename with
    # .wav extension because Whisper model only accepts certain file extensions.
    if not audio_file.endswith(".wav"):
        os.rename(audio_file, audio_file + ".wav")
        audio_file = audio_file + ".wav"

    # Open audio file and transcribe
    with open(audio_file, "rb") as f:
        transcript = speach_text(URL_SPEACH_TEXT,audio_file,LANG_SPEACH_TEXT)
    text_transcription = transcript["response"]

    return text_transcription


def chat_complete(
    text_input: str, messages: List[Dict[str, str]]
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Chat complete using OpenAI API. This is what generates stories.

    Args:
        text_input: Text to use as prompt for story generation
        messages: List of previous messages

    Returns:
        str: Generated story
        messages: Updated list of messages
    """
    # Init with prompt on first call
    if not messages:
        messages = [
            {
                "role": "system",
                "content": "Chat de pruebas para utilizar Bard API",
            }
        ]

    # Append to messages for chat completion
    messages.append({"role": "user", "content": text_input})

    # Fetch response from OpenAI
    print("Messages sent to call: ", messages)
    response =generate_response(messages,COOKIE_BARD)

    # Extract and store message
    system_message = dict(response["choices"][0]["message"])
    messages.append(system_message)

    # Return message to display
    display_message = system_message["content"]


    return display_message, messages



def audio_file_to_html(audio_file: str) -> str:
    """
    Convert audio file to HTML audio player.

    Args:
        audio_file: Path to audio file

    Returns:
        audio_player: HTML audio player that auto-plays
    """
    # Read in audio file to audio_bytes
    audio_bytes = io.BytesIO()
    with open(audio_file, "rb") as f:
        audio_bytes.write(f.read())

    # Generate audio player HTML object for autoplay
    audio_bytes.seek(0)
    audio = base64.b64encode(audio_bytes.read()).decode("utf-8")
    audio_player = (
        f'<audio src="data:audio/mpeg;base64,{audio}" controls autoplay></audio>'
    )
    return audio_player


def text_speech(input_text: str) -> str:
    """
    Use GCP Text-to-Speech API to convert text to a WAV file.

    Args:
        input_text: Text to convert to speech
        tts_voice_label: Label of voice to use, from keys of TTS_VOICE_OPTIONS in config

    Returns
        str: Path to output audio file
    """
    print(f"Convert text to speech: {input_text}")
    # set up the client object
    text_speach(URL_TEXT_SPEACH,input_text)

    # save the response audio as an MP3 file
    with open(GENERATED_SPEECH_PATH, "wb") as out:
        out.write(text_speach)

    # Generate audio player HTML object for autoplay
    audio_player = audio_file_to_html(GENERATED_SPEECH_PATH)

    return audio_player




"""
Gradio UI Definition
"""
with gr.Blocks() as demo:
    # Session state box containing all user/system messages, hidden
    messages = gr.State(list())

    # Initialize TTS
    tts_fn = None
    #tts_fn = text_speech
    

    # Set up layout and link actions together
    with gr.Row():
        with gr.Column(scale=1):
            
            # Audio Input Box
            audio_input = gr.Audio(
                source="microphone", type="filepath", label="User Audio Input"
            )

            # User Input Box
            transcribed_input = gr.Textbox(label="Transcription")

            # Story Output Box
            story_msg = gr.Textbox(label="Story")

            if tts_fn:
                # Connect story output to audio output after calling TTS on it
                html = gr.HTML()
                story_msg.change(tts_fn, [story_msg], html)


    # Connect audio input to user input
    audio_input.change(transcribe_audio, audio_input, transcribed_input)

    # Connect user input to story output
    transcribed_input.change(
        chat_complete, [transcribed_input, messages], [story_msg, messages]
    )


demo.launch()

