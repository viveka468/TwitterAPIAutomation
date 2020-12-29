def get_video_url(response_json):
    """Extract first video URL from the tweet response"""
    try:
        return response_json["extended_entities"]["media"][0]["video_info"]["variants"][0]['url']
    except KeyError:
        return None


def replace_new_lines(data):
    return data.replace('\n', '').replace('\r', '')
