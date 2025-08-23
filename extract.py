import os
import requests
from dotenv import load_dotenv
import json

class Extractor:
    def __init__(self):
        self.__transformed_data = []
        load_dotenv()
        self.__CLIENT_ID = os.getenv("CLIENT_ID")
        self.__CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.__USER_PASSWORD = os.getenv("USER_PASSWORD")
        self.__USERNAME = os.getenv("USERNAME")
    def extract(self):
        try:
            auth = requests.auth.HTTPBasicAuth(self.__CLIENT_ID, self.__CLIENT_SECRET)
            data = {
                'grant_type': 'password',
                'username': self.__USERNAME,
                'password': self.__USER_PASSWORD
            }
            headers = {"User-Agent": "reddit-pipeline/0.1"}

            response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
            response.raise_for_status()
            token = response.json()["access_token"]
            headers = {
                "Authorization": f"bearer {token}",
                "User-Agent": "reddit-pipeline/0.1"
            }

            after = None
            quantity = 200
            while len(self.__transformed_data) < quantity:
                response = requests.get("https://oauth.reddit.com/r/news/new", headers=headers, params={"limit": quantity if quantity < 100 else 100, 'after': after})
                self.__transformed_data.extend(response.json()["data"]["children"])
                after = response.json()["data"]["after"]
                if not after:
                    break

            with open("posts.json", "w") as f:
                f.write(json.dumps(self.__transformed_data, ensure_ascii=True, indent=4, separators=(",", ":")))
            return self.__transformed_data
        except requests.exceptions.HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

extractor = Extractor()
extractor.extract()