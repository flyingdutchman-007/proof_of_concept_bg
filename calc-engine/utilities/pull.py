import requests

class PullData:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            print(data)
            return data
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong: {err}")
            