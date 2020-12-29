from requests_oauthlib import OAuth1Session

from tests.util import app_properties


def get_oauth_1_request() -> OAuth1Session:
    auth_section = 'AuthenticationSection'
    client_id = app_properties.get_property(auth_section, 'client_id')
    client_secret = app_properties.get_property(auth_section, 'client_secret')
    resource_owner_key = app_properties.get_property(auth_section, 'resource_owner_key')
    resource_owner_secret = app_properties.get_property(auth_section, 'resource_owner_secret')

    oauth = OAuth1Session(
        client_id,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
    )
    return oauth
