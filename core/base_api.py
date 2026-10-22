import requests

from config import BASE_URL, TIMEOUT
from utils.helper import Helper

class BaseApi:
    def __init__(self) -> None:
        self.base_url = BASE_URL
        self.timeout = TIMEOUT
        self.session = requests.session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.helper = Helper()

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        self.helper.attach_response(response)
        return response

    def get(self, endpoin, **kwargs):
        return self._request("GET", endpoin, **kwargs)

    def post(self, endpoin, **kwargs):
        return self._request("POST", endpoin, **kwargs)

    def put(self, endpoin, **kwargs):
        return self._request("PUT", endpoin, **kwargs)

    def patch(self, endpoin, **kwargs):
        return self._request("PATCH", endpoin, **kwargs)

    def delete(self, endpoin, **kwargs):
        return self._request("DELETE", endpoin, **kwargs)

    def query(self, endpoin, **kwargs):
        return self._request("QUERY", endpoin, **kwargs)