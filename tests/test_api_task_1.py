import logging

import pytest
import wget

from tests.util import o_auth2_client as oauth2, file, request_util
from tests.util.app_constants import TWITTER_API_V1_URL, TWITTER_API_V2_URL
from tests.util.common import get_video_url, replace_new_lines

TEACH_FROM_HOME_TWEET_ID = '1257326183101980673'
TWEETS_BY_ID_URL = f'tweets?ids={TEACH_FROM_HOME_TWEET_ID}'
TWEETS_JSON_BY_ID_URL = f'statuses/show.json?id={TEACH_FROM_HOME_TWEET_ID}'
TWEETS_NATIVE_BY_ID_URL = f'statuses/show.json?id=1343927024214290438'
RETWEETS_URL = f'statuses/retweets/{TEACH_FROM_HOME_TWEET_ID}.json'
RETWEETERS_DETAIL_URL = f'statuses/retweeters/ids.json?id=' \
                        f'{TEACH_FROM_HOME_TWEET_ID}&stringify_ids=true&cursor='

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def global_data():
    return {'access_token': oauth2.get_access_token()}


def test_should_return_tweet_content_and_write_to_file(global_data):
    """Get the twitter content of the tweet https://twitter.com/Google/status/1257326183101980673
    and store it in a flat-file."""
    tweet_content = get_tweet_content_by_id(global_data)
    if tweet_content:
        file.write_text_to_file(tweet_content, file.MODE_WRITE_PLUS)


def get_tweet_content_by_id(global_data):
    tweet_url = f'{TWITTER_API_V2_URL}{TWEETS_BY_ID_URL}'
    headers = request_util.create_headers(global_data['access_token'])
    response_json = request_util.get_response(tweet_url, headers=headers)
    LOGGER.debug(f'Request URL {tweet_url}, headers {headers}, response {response_json}')
    if response_json and response_json['data'] and response_json['data'][0]:
        return replace_new_lines(response_json['data'][0]['text'])


def test_should_download_video_in_tweet():
    """Download the video file from the tweet https://twitter.com/Google/status/1257326183101980673
    and store it in a folder.
    Twitter API does not return extended entities in response for non
    Twitter native videos(like in the tweet 1257326183101980673)
    as explained here https://twittercommunity.com/t/twitter-video-support-in-rest-and-streaming-api/31258/40.
    So unable to download it. Added the a test case to depict the download of Twitter native videos
    'test_should_download_native_video_in_tweet'
   """

    tweet_url = f'{TWITTER_API_V1_URL}{TWEETS_JSON_BY_ID_URL}'
    response_json = request_util.get_response_using_oauth1(tweet_url)
    video_url = get_video_url(response_json)
    LOGGER.debug(f'Request URL {tweet_url}, response {response_json}, '
                 f'video URL {video_url}')
    if video_url:
        LOGGER.debug(f'Attempting to download video from {video_url}')
        wget.download(video_url, out=file.TWEET_RESULTS_DIRECTORY)
    else:
        LOGGER.warning('No Twitter native video is found')


def test_should_download_native_video_in_tweet():
    """Download the video file from the tweet https://twitter.com/Google/status/1257326183101980673
    and store it in a folder."""

    tweet_url = f'{TWITTER_API_V1_URL}statuses/show.json?id=1343927024214290438'
    response_json = request_util.get_response_using_oauth1(tweet_url)
    video_url = get_video_url(response_json)
    LOGGER.debug(f'Request URL {tweet_url}, response {response_json}, '
                 f'video URL {video_url}')
    if video_url:
        LOGGER.debug(f'Attempting to download video from {video_url}')
        wget.download(video_url)
    else:
        LOGGER.warning('No Twitter native video is found')


def test_get_number_of_retweets():
    """Get the number of retweets for the tweet https://twitter.com/Google/status/1257326183101980673
    and store it in the same file."""
    retweet_count = get_number_of_tweet()
    if retweet_count:
        file.write_text_to_file(retweet_count, file.MODE_APPEND)


def get_number_of_tweet():
    retweet_url = f'{TWITTER_API_V1_URL}{RETWEETS_URL}'
    response_json = request_util.get_response_using_oauth1(retweet_url)
    LOGGER.debug(f'Request URL {retweet_url}, response {response_json}')
    if response_json:
        return response_json[0]['retweet_count']


def test_should_get_re_tweeters_id(global_data):
    """Get the retweeters ID for the tweet https://twitter.com/Google/status/1257326183101980673
    and store it in the same file.
    NOTE:: This API returns only the active users, so it will not always match with the retweets count as specified in
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-retweeters-ids"""

    all_retweeters_id = get_all_retweeters_id(global_data)
    file.write_text_to_file(all_retweeters_id, file.MODE_APPEND)


def get_all_retweeters_id(global_data):
    all_retweeters_id = []
    headers = request_util.create_headers(global_data['access_token'])
    cursor = -1
    while True:
        retweeters_url = f'{TWITTER_API_V1_URL}{RETWEETERS_DETAIL_URL}{cursor}'
        response_json = request_util.get_response(retweeters_url, headers=headers)
        if response_json:
            cursor = response_json['next_cursor']
            all_retweeters_id.extend(response_json['ids'])
            LOGGER.debug(f'Request URL {retweeters_url}, response {response_json}')
            if cursor == 0:
                break
    return all_retweeters_id


def test_all_the_above_cases_using_flat_file(global_data):
    file_contents = file.read_all_lines()
    tweet_content = get_tweet_content_by_id(global_data)
    retweet_count = get_number_of_tweet()
    all_retweeters_id = get_all_retweeters_id(global_data)

    assert replace_new_lines(tweet_content) == replace_new_lines(file_contents[0])
    assert retweet_count == int(file_contents[1])
