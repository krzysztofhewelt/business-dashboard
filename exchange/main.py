import datetime
import requests

# https://docs.openexchangerates.org/reference/historical-json
API_URL = "https://openexchangerates.org/api"
HISTORICAL = "historical"
APP_ID = ""
FROM = "2024-04-25"
TO = "2021-09-08"
SYMBOLS = "PLN,EUR,USD,GBP,SEK,NOK,CHF,JPY"


def get_exchange_rate(date: str):
    url = f"{API_URL}/{HISTORICAL}/{date}.json?app_id={APP_ID}&symbols={SYMBOLS}"
    response = requests.get(url)

    print(date, response)

    return response.json()


today = datetime.date(year=2024, month=4, day=25)
to = datetime.date(year=2021, month=9, day=8)
one_day_delta = datetime.timedelta(days=1)

file = open("currencies.csv", "a", encoding="UTF-8")

while today >= to:
    rates = get_exchange_rate(today)["rates"]

    row = f"{today},{rates['PLN']},{rates['EUR']},{rates['USD']},{rates['GBP']},{rates['SEK']},{rates['NOK']},{rates['CHF']},{rates['JPY']}"
    file.write(row + "\n")
    today = today - one_day_delta

file.close()
