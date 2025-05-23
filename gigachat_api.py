import json
import streamlit as st

import requests


class Giga:
    _AUTHORIZATION_KEY = st.secrets["AUTHORIZATION_KEY"]

    @classmethod
    def get_access_token(cls) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '8e681e30-c78a-423e-8ec0-be38078b6f62',
            'Authorization': f'Basic {cls._AUTHORIZATION_KEY}'
        }
        response = requests.post(url, headers=headers, data=payload)

        return response.json()['access_token']


    @classmethod
    def send_promt(cls, access_token: str, msg: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps(
            {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": msg
                    }],
                "function_call": "auto"
            })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'RqUID': '8e681e30-c78a-423e-8ec0-be38078b6f62',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.post(url, headers=headers, data=payload)

        return response.json()['choices'][0]['message']['content'], response.json()['usage']['total_tokens']

    @classmethod
    def get_images(cls, access_token: str, img_id: str):
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{img_id}/content"

        payload = {}

        headers = {
            'Accept': 'application/jpg',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers, data=payload)

        return response.content
