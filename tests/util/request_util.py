import requests

from tests.model.request_exception import RequestException
from tests.util import o_auth_1_client as oauth1

REQUEST_GET = "GET"
REQUEST_POST = "POST"


def create_headers(access_token):
    if not access_token or len(access_token) == 0:
        raise Exception("Access token is mandatory to access API")
    headers = {"Authorization": "Bearer {}".format(access_token)}
    return headers


def get_response(url, headers):
    response = requests.get(url, headers=headers)
    check_if_response_ok(response)
    return response.json()


def get_response_using_oauth1(url):
    response = oauth1.get_oauth_1_request().get(url)
    print(response.status_code)
    response_json = response.json()
    check_if_response_ok(response)
    return response_json


def post_using_oauth1(url, params):
    response = oauth1.get_oauth_1_request().post(url, params=params)
    response_json = response.json()
    check_if_response_ok(response)
    return response_json


def check_if_response_ok(response):
    if response.status_code != 200:
        raise RequestException(response.status_code, response.text)
