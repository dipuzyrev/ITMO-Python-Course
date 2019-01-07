import requests
import time
from typing import Dict, Optional, List
from api_models import User, Message
from pprint import pprint

import config


def get(url: str, params: Dict = {}, timeout: int = 5, max_retries: int = 5, backoff_factor: float = 0.3) -> requests:
    """ Perform get request

    :param url: website address to perform request
    :param params: request parameters
    :param timeout: max waiting time from server's response
    :param max_retries: max number of request attempts
    :param backoff_factor: coefficient of exponential increase of delay between request attempts
    :return request result or raise exception
    """
    for retry in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            return r
        except requests.exceptions.RequestException:
            if retry == max_retries - 1:
                raise
        backoff_value = backoff_factor * (2 ** retry)
        time.sleep(backoff_value)


def get_friends(user_id: int, fields: str = "") -> Optional[User]:
    """ Get user's friends

    :param user_id: user ID for whom we are getting friends
    :param fields: additional information we want to get about user's friends
    :return List of user's friend
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'fields': fields,
        'v': config.VK_CONFIG['version']
    }

    response = get(config.VK_CONFIG['domain'] + "/friends.get", query_params).json()
    if not ('error' in response):
        friends = []
        for friend in response['response']['items']:
            friends.append(friend)
        return friends
    else:
        print('Error: ', response['error']['error_msg'])
        return []


def messages_get_history(user_id: int, offset: int = 0, count: int = 20) -> List[Message]:
    """  Get user messages history

    :param user_id: user ID with which we want to get messages
    :param offset: offset from last message
    :param count: count of messages
    :return: json object with messages
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': min(count, 200),
        'v': config.VK_CONFIG['version']
    }

    messages = []
    while count > 0:
        response = get(config.VK_CONFIG['domain'] + "/messages.getHistory", query_params)
        if response:
            result = response.json()
            if 'error' in result:
                print(result['error']['error_msg'])
            else:
                for message in result['response']['items']:
                    messages.append(Message(**message))
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['count'] = min(count, 200)

    return messages
