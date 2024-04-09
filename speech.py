import requests
import json
import os
import shutil

class Speach:
    # Constructor
    def __init__(self, url,context):
        self.url = url
        self.context = context

        
    def request(self):
        params = {'context': self.context,'lang': 'es'}
        response = download_file(self.url,params)
        return response



def download_file(url,params):
    
    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    local_filename = "generated_speech.mp3"
    with requests.get(url,params=params,headers=headers, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


if __name__ == "__main__":
  params = {'context': 'La inteligencia artificial (IA), en el contexto de las ciencias de la computación, es una disciplina y un conjunto de capacidades cognoscitivas e intelectuales expresadas por sistemas informáticos o combinaciones de algoritmos cuyo propósito es la creación de máquinas que imiten la inteligencia humana para realizar tareas, y que pueden mejorar conforme recopilan información.1​2​ A diferencia de la inteligencia sintética, la inteligencia artificial no tiene como finalidad reemplazar a los humanos, sino mejorar significativamente las capacidades y contribuciones de estos','lang': 'es'}
  url="http://localhost:8082/audio"
  response = download_file(url,params)
  os.system(f"start {response}") 
  
