import requests
import pprint
import time
from typing import Optional, Dict
from datetime import datetime
from statistics import median

domain = "https://api.vk.com/method"
access_token = "927a160a979d250ec7f611b4e3810ef3cda21a6e543a67f626c6052570291e152b3d7d1e270b894af1301"
my_id = 360784808


def get_friends(user_id: int, fields: str = "") -> Optional:
    """ Returns a list of user IDs or detailed information about a user's friends

    :param user_id: user ID for whom we getting friends
    :param fields: information we want to get about user's friends
    :return List of user's friend or error info from VK API
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'v': 5.53
    }

    response = get(domain + "/friends.get", query_params).json()
    try:
        return response['response']['items']
    except:
        pprint.pprint(response)
        return response


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


def age_predict(user_id: int) -> float:
    """ Returns median from user's friends ages

    :param user_id: user ID which age we are predicting
    :return: approximate user's age
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    age_list = []
    user_friends = get_friends(user_id, 'bdate')
    for friend in user_friends:
        try:
            friend_bdate = datetime.strptime(friend['bdate'], "%d.%m.%Y")
            today = datetime.now()
            age = (today - friend_bdate)
            age_list.append(age.days / 365.25)
        except:
            pass

    return round(median(age_list), 1) if age_list else None


if __name__ == "__main__":
    print(age_predict(my_id))
