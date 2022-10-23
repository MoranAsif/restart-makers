import datetime
import requests


def get_calender_events_list():
    timeMin = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)
    timeMax = timeMin + datetime.timedelta(days=9)
    timeMin = timeMin.strftime("%Y-%m-%dT%H:%M:%S-00:00")
    timeMax = timeMax.strftime("%Y-%m-%dT%H:%M:%S-00:00")

    # ------------ prod-------------:
    user = "xxx@gmail.com"
    api_key = "xxx"

    url = (
        f"https://www.googleapis.com/calendar/v3/calendars/{user}/events?key={api_key}&timeMax={timeMax}&timeMin={timeMin}"
    )
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()