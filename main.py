import requests
import json
from typing import NamedTuple
from datetime import datetime, timedelta, date
from usage_metrics import Usage_Metrics
import jsonpickle
import time


class Config:
    user: str
    pwd: str
    meterId: str


LOGIN_URL = "https://smartmeter.netz-noe.at/orchestration/Authentication/Login"
USAGE_URL = "https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day"
CONFIG_PATH = "./config.json"
CONFIG: Config = None


def load_config():
    with open(CONFIG_PATH, "r") as file:
        configDict = json.load(file)
        config = Config()
        config.user = configDict["user"]
        config.password = configDict["password"]
        config.meterId = configDict["meterId"]
        global CONFIG
        CONFIG = config


def pull_data(day: datetime) -> dict:
    session = requests.Session()
    login = session.post(LOGIN_URL, json={"user": CONFIG.user, "pwd": CONFIG.password})
    usage = session.get(
        USAGE_URL,
        params={"meterId": CONFIG.meterId, "day": yesterday.strftime("%Y-%m-%d")},
    )
    return usage.json()


def write_usage(day: datetime, usage: dict):
    with open(f"./usage_files/usage_{yesterday}.json", "w") as usage_file:
        json.dump(usage, usage_file)


def get_usage_data(day: datetime):
    usage_json = pull_data(yesterday)
    write_usage(yesterday, usage_json)
    return usage_json


def generate_timestamps(day: datetime):
    # Initialize the start time for the given date
    start_time = datetime.combine(day, datetime.min.time())

    # Initialize an empty list to store timestamps
    timestamps = []

    # Generate timestamps every fifteen minutes until the end of the day
    while start_time.date() == day:
        timestamps.append(start_time)
        start_time += timedelta(minutes=15)

    return timestamps


def parse_usage(timestamps: list[datetime], usage: dict):
    usages = [
        Usage_Metrics(ts, usage["meteredValues"][i], usage["meteredPeakDemands"][i])
        for i, ts in enumerate(timestamps)
    ]
    return usages


def load_usage_file(day):
    with open(f"./usage_files/usage_2023-11-18.json", "r") as file:
        return json.load(file)


def write_usage_to_file(usage_metrics: Usage_Metrics):
    with open("./15min.txt", "a") as fifteen_min_log:
        usage_json = jsonpickle.encode(usage_metrics, unpicklable=False)
        fifteen_min_log.write(f"{usage_json}\n")


def push_usage_values(usage_values: list[Usage_Metrics]):
    for usage_metric in usage_values:
        write_usage_to_file(usage_metric)
        time.sleep(2)


def get_last_15_minute_mark(input_datetime):
    # Calculate the number of minutes since the last 15-minute mark
    minutes_past_last_15_minute_mark = input_datetime.minute % 15

    # Subtract the minutes to get the last 15-minute mark
    last_15_minute_mark = input_datetime - timedelta(
        minutes=minutes_past_last_15_minute_mark
    )

    # Set seconds and microseconds to 0 for accuracy
    last_15_minute_mark = last_15_minute_mark.replace(second=0, microsecond=0)

    return last_15_minute_mark

def write_daily_usage_data(usage_metrics: list[Usage_Metrics]):
    with open("./daily.txt", "a") as daily_log:
        usage_json = jsonpickle.encode(usage_metrics, unpicklable=False)
        daily_log.write(f"{usage_json}\n")

load_config()
yesterday = date.today() - timedelta(days=1)
# usagedata = load_usage_file(yesterday)
usage_data = get_usage_data(yesterday)
usage_metrics = parse_usage(generate_timestamps(yesterday), usage_data)
# push_usage_values
write_daily_usage_data(usage_metrics)

print(a)
# usage_json = get_usage_data()
