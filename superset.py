import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()

host = os.getenv('SUPPERSET_HOST')
username = os.getenv('SUPPERSET_USERNAME')
password = os.getenv('SUPPERSET_PASSWORD')



class Superset():
    def __init__(self, host=host, username=username, password=password) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.access_token = self.get_access_token()

    def get_access_token(self):
        payload = {
            "username" : self.username,
            "password" : self.password,
            "provider" : "db"
        }

        r = requests.post(self.host + "/security/login", json=payload)
        access_token = r.json()['access_token']

        return {"Authorization": f"Bearer {access_token}"}
    
    def get_dashboard(self, id):
        endpoint = f"{self.host}dashboard/{id}"

        return requests.get(endpoint, headers=self.access_token).json()
    
    def export_dashboard(self, id):
        endpoint = f"{self.host}dashboard/export/?q=!({id})"


        response = requests.get(endpoint)    
        response.encoding = 'utf-8'
        return response

    def get_chart(self, id):
        endpoint = f"{self.host}chart/{id}"
        return requests.get(endpoint, headers=self.access_token).json()        

    def export_chart(self, id):
        endpoint = f"{self.host}chart/export/?q=!({id})"

        response = requests.get(endpoint)    
        response.encoding = 'utf-8'
        return response

    def get_dataset(self, id):  
        endpoint = f"{self.host}dataset/{id}"
        return requests.get(endpoint, headers=self.access_token).json()    


if __name__ == "__main__":
    ss = Superset()
    print(ss.export_dashboard(2))


    

