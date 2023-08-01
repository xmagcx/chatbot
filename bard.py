import requests



class Bard:
    # Constructor
    def __init__(self, url,session_id,message):
        self.url = url
        self.session_id = session_id
        self.message = message
        
    def request(self):
        payload = {
            "session_id": self.session_id,
            "message": self.message 
        }
        
        response = requests.request("POST", self.url, json=payload)
        return response



if __name__ == "__main__":
    url = "http://localhost:8080/ask"
    session_id ="ZAirF-Ur-UgrJjsy7JQtpdycxIvG1pX_KucTypvPp5dXMPbNggOBBbO_x6MREM5OXUJ4kQ." #use your cookie value for __Secure-1PSID

    payload = {
        "session_id": session_id,
        "message": "Cual es el centro de Chile?"
    }
    response = requests.request("POST", url, json=payload)



    print("Status Code: ", response.status_code)
    print("JSON Response: ", response.text)



