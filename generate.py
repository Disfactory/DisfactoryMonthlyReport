import requests
import os
from datetime import datetime

API = "http://api.disfactory.tw/api/statistics/factories?display_status={}&level=city"

STATUS_LIST = [
    "已檢舉",
    "已排程稽查",
    "陳述意見期",
    "已勒令停工",
    "已發函斷電",
    "已排程拆除",
    "已拆除",
    "不再追蹤",
]


def status_count(file_path):
    result = {}

    for status_item in STATUS_LIST:
        url = API.format(status_item)
        resp = requests.get(url)
        data = resp.json()
        for key, value in data["cities"].items():
            if key not in result:
                result[key] = {}

            result[key][status_item] = value["factories"]

    lines = []
    lines.append("city, " + ",".join(STATUS_LIST))
    for key, values in result.items():
        city = key
        data = []
        for status_item in STATUS_LIST:
            data.append(str(values[status_item]))

        lines.append(f"{city}, " + ",".join(data))

    with open(file_path, "w") as fp:
        fp.write("\n".join(lines))



def report_record_count(file_path):
    url = "https://api.disfactory.tw/api/statistics/factories?level=city"

    resp = requests.get(url)
    data = resp.json()

    lines = []
    lines.append("city, report_records")
    cities = data["cities"]
    for key, values in cities.items():
        lines.append(f"{key}, {values['report_records']}")

    with open(file_path, "w") as fp:
        fp.write("\n".join(lines))

def get_this_month_str():
    return datetime.today().strftime("%Y-%m") 


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    folder_path = os.path.join(BASE_DIR, get_this_month_str())

    os.makedirs(folder_path, exist_ok=True)
    status_count(os.path.join(folder_path, "status.csv"))
    report_record_count(os.path.join(folder_path, "report_records.csv"))
