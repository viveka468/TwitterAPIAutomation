import json
import os

MODE_WRITE_PLUS = 'w+'
MODE_APPEND = 'a'

TWEET_RESULTS_DIRECTORY = 'results'
TWEET_RESULTS_FILE_NAME = 'tweet.txt'
TWEET_RESULTS_FILE = TWEET_RESULTS_DIRECTORY + '/' + TWEET_RESULTS_FILE_NAME


def write_json_to_flat_file(data, mode):
    createDirectoryIfNotExists()
    with open(TWEET_RESULTS_FILE, mode) as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)


def write_text_to_file(data, mode):
    createDirectoryIfNotExists()
    with open(TWEET_RESULTS_FILE, mode) as f:
        f.write(f'{str(data)}\n')


def read_all_lines():
    with open(TWEET_RESULTS_FILE, "r") as f:
        return f.readlines()


def createDirectoryIfNotExists():
    if not os.path.exists(TWEET_RESULTS_DIRECTORY):
        os.mkdir(TWEET_RESULTS_DIRECTORY)
