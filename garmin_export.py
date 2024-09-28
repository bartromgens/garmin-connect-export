import argparse
import csv
from typing import Any
from typing import List

import requests
import datetime


class GarminClient:
    URL_REST_HEART_RATE = "https://connect.garmin.com/usersummary-service/stats/heartRate/daily/{begin}/{end}"
    URL_HRV = "https://connect.garmin.com/hrv-service/hrv/daily/{begin}/{end}"

    def __init__(self, authorization_header: str, cookie_header: str):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": authorization_header,
            "Cookie": cookie_header,
            "DI-Backend": "connectapi.garmin.com",
        }

    def get_rest_heart_rate(self, date_begin: datetime.date, date_end: datetime.date):
        url = self.URL_REST_HEART_RATE.format(begin=date_begin, end=date_end)
        response = requests.get(url, headers=self.headers)
        return {
            date["calendarDate"]: date["values"]["restingHR"]
            for date in response.json()
        }

    def get_hrv(self, date_begin: datetime.date, date_end: datetime.date):
        url = self.URL_HRV.format(begin=date_begin, end=date_end)
        response = requests.get(url, headers=self.headers)
        return {
            date["calendarDate"]: date["lastNightAvg"]
            for date in response.json()["hrvSummaries"]
        }


def main():
    args = parse_args()
    date_begin = args.start_date
    date_end = args.end_date if args.end_date else datetime.date.today()

    client = GarminClient(
        authorization_header=args.auth_header, cookie_header=args.cookie_header
    )

    heart_rates = {}
    hrv = {}
    while date_begin < date_end:
        date_end_page = date_begin + datetime.timedelta(days=25)
        print(f"Getting data for {date_begin} : {date_end_page}")
        heart_rates.update(client.get_rest_heart_rate(date_begin, date_end_page))
        hrv.update(client.get_hrv(date_begin, date_end_page))
        date_begin = date_end_page

    date_rate_hrv = [
        [date, heart_rates.get(date, ""), hrv.get(date, "")]
        for date in sorted(heart_rates.keys())
    ]

    print(date_rate_hrv)
    write_to_csv(date_rate_hrv, ["date", "rest heart rate", "HRV"], args.fileout)


def write_to_csv(rows: List[Any], headers: List[str], filename: str) -> None:
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)


def valid_date(s) -> datetime.date:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Not a valid date: {s}. Use format YYYY-MM-DD."
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Retrieve Garmen Connect data and write them to a CSV file."
    )
    parser.add_argument(
        "--start-date",
        required=True,
        type=valid_date,
        help="Start date in the format YYYY-MM-DD (e.g., 2024-08-01)",
    )
    parser.add_argument(
        "--end-date",
        type=valid_date,
        help="End date in the format YYYY-MM-DD (e.g., 2024-08-01). Optional.",
    )
    parser.add_argument(
        "--fileout", required=True, type=str, help="File path for the CSV output file"
    )
    parser.add_argument(
        "--auth-header",
        required=True,
        type=str,
        help="Authorization header taken from the web app.",
    )
    parser.add_argument(
        "--cookie-header",
        required=True,
        type=str,
        help="Cookie header taken from the web app.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
