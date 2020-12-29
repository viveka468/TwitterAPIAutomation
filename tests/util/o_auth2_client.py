import requests

from tests.util import app_properties


def get_access_token():
    """ Returns access token using OAuth2.0 with client credentials"""
    auth_section = 'AuthenticationSection'
    grant_type = 'client_credentials'

    token_url = app_properties.get_property(auth_section, 'token_url')
    client_id = app_properties.get_property(auth_section, 'client_id')
    client_secret = app_properties.get_property(auth_section, 'client_secret')
    response = requests.post(token_url,
                             auth=(client_id, client_secret),
                             data={'grant_type': grant_type,
                                   'client_id': client_id, 'client_secret': client_secret})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise RuntimeError("Unable to fetch Access token")
