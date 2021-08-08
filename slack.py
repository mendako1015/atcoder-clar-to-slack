#!/usr/bin/env python3

import requests

class Slack:
    session = None
    HEADERS = {
        'Content-type': 'application/json'
    }

    def __init__(self):
        self.session = requests.session()
    
    def send_message(self, webhook_url, json):
        response = self.session.post(webhook_url,
                                     data = json,
                                     headers = self.HEADERS)
        response.raise_for_status()