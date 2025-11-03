import requests

DEFAULT_HEADERS: dict = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class BaseThirdPartyAPIService:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers if headers else DEFAULT_HEADERS

    def post(self, endpoint: str, data: dict = None, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
