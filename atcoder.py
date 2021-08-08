#!/usr/bin/env python3

import json, requests
from bs4 import BeautifulSoup

class Atcoder:
    session = None
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Authority': ''
    }

    def __init__(self):
        self.session = requests.session()

    def login(self, username, password):
        login_data = {
            "username": username,
            "password": password
        }
        login_url = "https://atcoder.jp/login"

        # Get csrf_token
        response = self.session.get(login_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        login_data["csrf_token"] = soup.find("input", attrs = {"name": "csrf_token"})["value"]

        # Login
        response = self.session.post(login_url,
                                     data = login_data,
                                     headers = self.HEADERS)
        response.raise_for_status()

    def load_clar_page(self, clar_url):
        response = self.session.get(clar_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.find("tbody").find_all("tr")
        clars = []
        for tr in trs:
            tds = tr.find_all("td")
            clar = Clar()
            clar.task = tds[0].get_text().strip()
            if tds[0].find("a") is not None:
                clar.task_url = tds[0].find("a")["href"]
            clar.username = tds[1].get_text().strip()
            clar.question = tds[2].get_text().strip()
            clar.reply = tds[3].get_text().strip()
            clar.public = tds[4].get_text().strip()
            clar.submission_time = tds[5].get_text().strip()
            clar.update_time = tds[6].get_text().strip()
            clar.clar_url = tds[7].find("a")["href"]
            clars.insert(0, clar)
        return clars

class Clar:
    task = ""
    task_url = ""
    username = ""
    question = ""
    reply = ""
    public = False
    submission_time = ""
    update_time = ""
    url = ""
    clar_url = ""

    def __eq__(self, other):
        return self.update_time == other.update_time

    def convert_json(self, updated):
        if not updated:
            return json.dumps({
                'attachments':[
                    {
                        'color': '#DAA038',
                        'fallback': '新しい質問が来ました',
                        'fields': [
                            {
                                'value': '<!here> 新しい質問が来ました',
                            },
                            {
                                'value': '*%s* (%s)'
                                    % ('<https://atcoder.jp%s|%s>'
                                        % (self.task_url, self.task)
                                        if len(self.task) > 4 else 'コンテスト全体の質問',
                                    self.username),
                            },
                            {
                                'title': '【質問】',
                                'value': self.question,
                            },
                        ],
                        'actions': [
                            {
                                "type": "button",
                                "text": "回答する",
                                "url": 'https://atcoder.jp' + self.clar_url
                            }
                        ],
                        'footer': self.update_time
                    }
                ]
            })
        else:
            return json.dumps({
                'attachments':[
                    {
                        'color': '#2EB886',
                        'fallback': '質問の回答を更新しました',
                        'fields': [
                            {
                                'value': '質問の回答を更新しました',
                            },
                            {
                                'value': '*%s* (%s)'
                                    % ('<https://atcoder.jp%s|%s>'
                                        % (self.task_url, self.task)
                                        if len(self.task) > 4 else 'コンテスト全体の質問',
                                    self.username),
                            },
                            {
                                'title': '【質問】',
                                'value': self.question,
                            },
                            {
                                'title': '【回答】',
                                'value': self.reply,
                            },
                            {
                                'title': '【全体公開】',
                                'value': self.public,
                            },
                        ],
                        'footer': self.update_time
                    }
                ]
            })