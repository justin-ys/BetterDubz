import requests

class W2LException(Exception):
    pass

class W2LAPI():
    def __init__(self, url, key):
        self.url = url
        self.key = key
        pass
    def get_dubbed(self, audio, video):
        return