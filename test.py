from bard import Bard
import json


URL_BARD = "http://192.168.1.156:8080/ask"
COOKIE_BARD = "ZAirF-Ur-UgrJjsy7JQtpdycxIvG1pX_KucTypvPp5dXMPbNggOBBbO_x6MREM5OXUJ4kQ."
URL_SPEACH_TEXT = "http://192.168.1.156:8081/uploadfile/"
LANG_SPEACH_TEXT = "es-ES"
URL_TEXT_SPEACH  = "http://192.168.1.156:8082/audio"
GENERATED_SPEECH_PATH = "generated_speech.mp3"


def clean_text (text):
    text = text.replace("\\n", " ").replace('"',"").replace("*","")
    return text


def generate_response(prompt_input,idbard):
    normalized=""
    
    model = Bard(URL_BARD,idbard,prompt_input)
    response = model.request()

    
    if response.status_code == 200:
        normalized = clean_text(response.text)
        #print(normalized)
    else:
        normalized = "Hay un problema con mi Modelo"
    return normalized


response = generate_response("quien eres?",COOKIE_BARD)
dictionary ={}

dictionary = dict({'content':response})

print(dictionary["content"])