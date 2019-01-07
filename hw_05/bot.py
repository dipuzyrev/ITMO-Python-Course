import requests
import config
import telebot
from typing import Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup


DAYS = {
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
    'sunday': 7}

DAYS_RUS = {
    1: 'в понедельник',
    2: 'во вторник',
    3: 'в среду',
    4: 'в четверг',
    5: 'в пятницу',
    6: 'в субботу',
    7: 'в воскресенье'
}


bot = telebot.TeleBot(config.access_token)


def get_page(group: str, week: str = '') -> str:
    """ Get page source from ITMO university website by group number and week parity

    :param group: user's academic group
    :param week: 0 - all schedule, 1 - even, 2 - odd
    :return: page's HTML code
    """
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page: str, day: int) -> Optional[Tuple]:
    """ Parse schedule HTML page to get certain day lessons

    :param web_page: page's HTML code
    :param day: what day to parse - from 1 (monday) to 7 (sunday)
    :return: 5 lists with this information about day lessons - time, parity, location, room, subject
    """
    soup = BeautifulSoup(web_page, "html5lib")
    day_attr = str(day) + 'day'

    try:
        # Получаем таблицу с расписанием на указанный день
        schedule_table = soup.find("table", attrs={"id": day_attr})

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        #parity
        parities_list = schedule_table.find_all("td", attrs={"class": "time"})
        parities_list = [parity.dt.text for parity in parities_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Get lesson room
        rooms_list = schedule_table.find_all("dd", attrs={"class": "rasp_aud_mobile"})
        rooms_list = [room.text for room in rooms_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [(lesson.dd.text.strip(), lesson.dt.b.text.strip()) for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    except AttributeError:
        return None

    return times_list, parities_list, locations_list, rooms_list, lessons_list


def send_help(chat_id: int) -> None:
    """ Send help to user if his query is incorrect

    :param chat_id: chat ID
    :return: nothing
    """
    commands = [
        '<b>/near</b> group',
        '<b>/day</b> week group',
        '<b>/tomorrow</b> group',
        '<b>/all</b> week group']

    bot.send_message(chat_id, "Прости, но меня научили отвечать только на такие команды:\n\n" +
                     "\n".join(commands), parse_mode='HTML')


def print_lesson(schedule: Optional[Tuple], i: int) -> str:
    """ Generate 1 lesson HTML code for user

    :param schedule: 5 specified lists about certain day lessons info
    :param i: lesson number
    :return: generated 1 lesson HTML code for user
    """
    if schedule is None or i >= len(schedule[0]) or i < 0:
        return None

    times_lst, parities_lst, locations_lst, rooms_lst, lessons_lst = schedule
    printed = ''
    parity = "({}), ".format(parities_lst[i]) if parities_lst[i] else ""
    if locations_lst[i] and rooms_lst[i]:  # general case
        printed += '<b>{}</b> {}{}, {}, {}\n\n'.\
            format(times_lst[i], parity, locations_lst[i], rooms_lst[i], lessons_lst[i])
    else:  # online lesson
        printed += '<b>{}</b> {}{}\n\n'.format(times_lst[i], parity, lessons_lst[i])

    return printed


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Get schedule on certain day

    :param message: user's message data
    :return: nothing
    """

    query = message.text.split()
    day = query[0][1:]
    week = 0
    group = ''

    if len(query) == 1:
        send_help(message.chat.id)
        return False
    elif len(query) == 3:
        week = query[1]
        group = query[2]
    elif len(query) == 2:
        group = query[1]

    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, DAYS[day])

    if schedule is None:
        bot.send_message(message.chat.id, 'Сайт ИТМО ничего не дает. Если группа указана верно, значит это выходной.')
        return False

    resp = '<b>{}:</b>\n\n'.format(DAYS_RUS[DAYS[day]].capitalize())
    for i in range(len(schedule[0])):
        resp += print_lesson(schedule, i)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Get next lesson

    :param message: user's message data
    :return: nothing
    """

    query = message.text.split()
    group = ''

    if len(query) == 1:
        send_help(message.chat.id)
        return False

    group = query[1]

    week = (datetime.today().isocalendar()[1] % 2) + 1
    day = datetime.today().isocalendar()[2]

    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, day)

    lesson_index = None
    if schedule is not None:
        times_list = schedule[0]
        for i in range(len(times_list)):
            if times_list[i] != "День":
                start_time = times_list[i].split('-')[0]
                start_time = datetime.strptime(start_time, "%H:%M").time()
                if start_time > datetime.now().time():
                    lesson_index = i
                    break

    if lesson_index is None:
        for i in range(15):
            day = (day % 7) + 1  # sunday to monday, other days just +1
            week = (week % 2) + 1 if day == 1 else week  # if it is monday, change week value

            web_page = get_page(group, week)
            schedule = parse_schedule(web_page, day)

            if schedule is not None:
                times_list = schedule[0]
                for j in range(len(times_list)):
                    if times_list[j] != "День":
                        lesson_index = j
                        break

            if lesson_index is not None:
                break

    if lesson_index is not None:

        resp = '<b>{} в </b>'.format(DAYS_RUS[day].capitalize())
        lesson = print_lesson(schedule, 0)
        if (lesson is not None):
            resp += lesson
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return

    bot.send_message(message.chat.id, "Извини, я ничего не нашла :(")


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Get tomorrow schedule (or monday, if next day is sunday)

    :param message: user's message data
    :return: nothing
    """

    query = message.text.split()
    group = ''

    if len(query) == 1:
        send_help(message.chat.id)
        return False
    else:
        group = query[1]

    day = datetime.today().isocalendar()[2]
    next_day = day + 1 if (day + 1) < 7 else 1
    week = (datetime.today().isocalendar()[1] % 2) + 1
    week = (week % 2) + 1 if next_day == 1 else week

    new_command = '/'
    for week_day, day_number in DAYS.items():
        if day_number == next_day:
            new_command += week_day
            break
    new_command += ' ' + str(week) + ' ' + group
    message.text = new_command

    get_schedule(message)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Get week schedule

    :param message: user's message data
    :return: nothing
    """
    query = message.text.split()
    week = 0
    group = ''

    if len(query) == 1:
        send_help(message.chat.id)
        return False
    elif len(query) == 3:
        week = query[1]
        group = query[2]
    elif len(query) == 2:
        group = query[1]

    for day, weekday in DAYS_RUS.items():
        web_page = get_page(group, week)
        schedule = parse_schedule(web_page, day)

        if schedule is not None:
            resp = '<b>{}:</b>\n\n'.format(weekday.capitalize())
            for i in range(len(schedule[0])):
                resp += print_lesson(schedule, i)

            bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)

