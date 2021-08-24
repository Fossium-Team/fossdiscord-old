import json
import requests
import os
import time


class daemon:
    def __init__(self):
        self.datapath = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), 'cache')
        if not os.path.exists(self.datapath):
            os.mkdir(os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), 'cache'))
        self.catpic()
        self.dogpic()

    def catpic(self):
        catpicjson = os.path.join(self.datapath, 'catpic.json')
        data = requests.get('https://api.thecatapi.com/v1/images/search?limit=100&page=1&order=Desc').json()
        with open(catpicjson, 'w') as file:
            json.dump(data, file, indent=4)

    def dogpic(self):
        dogpicjson = os.path.join(self.datapath, 'dogpic.json')
        data = requests.get('https://api.thedogapi.com/v1/images/search?limit=100&page=1&order=Desc').json()
        with open(dogpicjson, 'w') as file:
            json.dump(data, file, indent=4)


def services():
    while True:
        daemon()
        time.sleep(1800)
