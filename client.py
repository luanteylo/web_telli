import requests


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://{}:{}/process'.format(self.host, self.port)
        self.response = None

    def send(self, action, value):
        # create data request

        data = {
            'action': action,
            'value': value
        }

        r = requests.post(self.url, timeout=10.0, json=data)
        self.response = r.json()