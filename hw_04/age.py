from datetime import datetime as dt
from statistics import median
import config
from typing import Optional
from api import get_friends
import pprint
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Returns median from user's friends ages

    :param user_id: user ID which age we are predicting
    :return: approximate user's age
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends_ages = []
    request = get_friends(user_id, 'bdate')
    user_friends = [User(**friend) for friend in request]
    pprint.pprint(user_friends)
    for friend in user_friends:
        if (friend.bdate is not None) and (len(friend.bdate) >= 8):
            friend_bdate = dt.strptime(friend.bdate, "%d.%m.%Y")
            today = dt.now()
            age = (today - friend_bdate)
            friends_ages.append(age.days / 365.25)

    return round(median(friends_ages), 1) if friends_ages else None


if __name__ == '__main__':
    print(age_predict(config.VK_CONFIG['my_id']))
