import requests
import json


class Transcribe:
    # Constructor
    def __init__(self, url,file,lang):
        self.url = url
        self.lang = lang
        self.file = file
        
        
    def request(self):
        params = {"language": self.lang}
        files = {'file': (open(self.file, 'rb'))}
        response = requests.request("POST", self.url, files=files,params=params)
        response_dict = response.json()
        return response_dict.get('response')


if __name__ == "__main__":
  
    params = {"language": "es-ES"}
    myurl = 'http://192.168.1.156:8081/uploadfile/'
    files = {'file': (open(r'greet.wav', 'rb'))}
    getdata = requests.post(myurl, files=files,params=params)
    #, files=files
    response_dict = getdata.json()
    print(response_dict.get('response'))