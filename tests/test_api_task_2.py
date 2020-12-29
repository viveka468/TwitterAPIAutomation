import logging

import pytest

from tests.model.request_exception import RequestException
from tests.util import request_util
from tests.util.app_constants import TWITTER_API_V1_URL

NEW_TWEET_URL = 'statuses/update.json'
RETWEET_URL = 'statuses/retweet/{id}.json'
RETWEETS_URL = 'statuses/retweets/{id}.json'
UN_RETWEET_URL = 'statuses/unretweet/{id}.json'
DELETE_TWEET_URL = 'statuses/destroy/{id}.json'

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def global_data():
    return {'new_tweet_id': 0}


def test_post_a_new_tweet(global_data):
    """Make a new tweet with the text "We welcome you to MSD family :)"""
    new_tweet_url = f'{TWITTER_API_V1_URL}{NEW_TWEET_URL}'
    post_params = {
        'status': 'We welcome you to MSD family :)',
    }
    response_json = request_util.post_using_oauth1(new_tweet_url, post_params)
    global_data['new_tweet_id'] = response_json['id']


def test_retweet(global_data):
    """Now retweet the same tweet."""
    tweet_id = global_data['new_tweet_id']
    retweet_url = f'{TWITTER_API_V1_URL}{RETWEET_URL.format(id=tweet_id)}'
    try:
        request_util.post_using_oauth1(retweet_url, None)
    except RequestException as e:
        LOGGER.error(f"Unable to retweet due to {e.message}")


def test_should_find_retweet_count_and_retweeters_ID(global_data):
    """Now get the retweet count & retweeters ID and validate the correctness of the data."""
    tweet_id = global_data['new_tweet_id']
    retweet_url = f'{TWITTER_API_V1_URL}{RETWEETS_URL.format(id=tweet_id)}'
    response_json = request_util.get_response_using_oauth1(retweet_url)
    if response_json:
        extract_user = lambda retweet: retweet['user']['id']
        retweeter_id_list = list(map(extract_user, response_json))
        LOGGER.debug(f"Retweeters list {retweeter_id_list}, retweets count {response_json[0]['retweet_count']}")
        assert len(retweeter_id_list) == response_json[0]['retweet_count']


def test_un_retweet_and_validate_data(global_data):
    """Now revert the previous retweet (un retweet the above tweet)
    and get the retweet count & retweeters ID and validate the correctness of the data."""
    tweet_id = global_data['new_tweet_id']
    un_retweet_url = f'{TWITTER_API_V1_URL}{UN_RETWEET_URL.format(id=tweet_id)}'
    request_util.post_using_oauth1(un_retweet_url, None)
    test_should_find_retweet_count_and_retweeters_ID(global_data)


def test_should_delete_tweet(global_data):
    """Now finally delete the tweet"""
    tweet_id = global_data['new_tweet_id']
    delete_tweet_url = f'{TWITTER_API_V1_URL}{DELETE_TWEET_URL.format(id=tweet_id)}'
    request_util.post_using_oauth1(delete_tweet_url, None)
