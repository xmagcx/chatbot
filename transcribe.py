import requests


class Transcribe:
    # Constructor
    def __init__(self, url,lang,file):
        self.url = url
        self.file = file
        self.lang = lang
        
    def request(self):
        params = {"language": self.lang}
        response = requests.request("POST", self.url, files=self.file,params=params)
        return response


if __name__ == "__main__":
  
    params = {"language": "es-ES"}
    myurl = 'http://localhost:8081/uploadfile/'
    files = {'file': (open(r'C:/Users/mauri/Downloads/IA.wav', 'rb'))}
    getdata = requests.post(myurl, files=files,params=params)
    #, files=files
    print(getdata.text)