import requests


class API:
    def __init__(self):
        self.base_url = "https://itunes.apple.com/search"

    def search(self, query):
        params = {"entity": "podcast", "term": query}
        req = requests.get("https://itunes.apple.com/search", params)
        json = filter(lambda entry: "feedUrl" in entry.keys(), req.json()["results"])
        entries = map(lambda entry: {"name": entry["collectionName"], "value": entry["feedUrl"]}, json)
        return list(entries)

    def fetch(self, feed_url, ):
    
