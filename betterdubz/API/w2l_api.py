import requests

class W2LException(Exception):
    pass

class W2LAPI():
    def __init__(self, url=None, key=None):
        self.url = "http://f478-35-197-117-131.ngrok.io/" + 'upload'
        self.key = key
        pass
    def get_dubbed(self, audio, video, output):
        files = {
            'face': open(video, 'rb'),
            'audio': open(audio, 'rb'),
        }
        response = requests.post(self.url, files=files)
        with open(output, "wb") as f:
            f.write(response.content)
