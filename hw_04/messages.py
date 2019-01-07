from collections import Counter
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple
from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Get messages dates and their frequencies

    :param messages: list of Messages
    """

    m_dates, m_counts = [], []
    frequency = Counter()
    for message in messages:
        message_date = fromtimestamp(message.date)
        frequency[message_date] += 1

    for date in frequency:
        m_dates.append(date)
        m_counts.append(frequency[date])

    return m_dates, m_counts


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Create plotly chart

    :param date: list of dates
    :param freq: list of messages numbers at certain dates
    """

    plotly.tools.set_credentials_file(username=config.PLOTLY_CONFIG['username'], api_key=config.PLOTLY_CONFIG['api_key'])
    data = [go.Scatter(x=dates, y=freq)]
    py.plot(data)


if __name__ == '__main__':
    messages_list = messages_get_history(364936790, 0, 1000)
    messages_stat = count_dates_from_messages(messages_list)
    plotly_messages_freq(messages_stat[0], messages_stat[1])
