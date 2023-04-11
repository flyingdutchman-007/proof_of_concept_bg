import json
import requests

class PushData:
    def __init__(self, url, mutation):
        self.mutation = mutation
        self.url = url

    def execute_mutation(self, data_json):
        json_data = json.loads(data_json)
        variable_values = {'input': json_data}
        requests.post(url=self.url, json={"query": self.mutation, "variables": variable_values})
        print(json_data)