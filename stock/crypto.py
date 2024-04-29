from urllib.request import urlopen
import certifi
import datetime
import json

FROM = "2020-01-01"
TO = "2024-04-24"
API_KEY = ""
PERIOD = "4hour"

NAMES = [
    "Bitcoin",
    "Ethereum",
    "Tether",
    "BNB",
    "Solana",
    "USDC",
    "XRP",
    "Dogecoin",
    "Toncoin",
]

SYMBOLS = ["BTC", "ETH", "USDT", "BNB", "SOL", "USDC", "XRP", "DOGE", "TON"]


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


# for i in range(0, len(SYMBOLS)):
#     SYMBOL = SYMBOLS[i]
#     NAME = NAMES[i]
#     url = f"https://financialmodelingprep.com/api/v3/historical-chart/{PERIOD}/{SYMBOL}?from={FROM}&to={TO}&apikey={API_KEY}"
#     print(url)


today = datetime.date(year=2024, month=4, day=25)
prev = datetime.timedelta(days=160)


for i in range(0, len(SYMBOLS)):
    today = datetime.date(year=2024, month=4, day=25)
    FROM = today - prev
    TO = today
    SYMBOL = SYMBOLS[i]
    NAME = NAMES[i]

    for i in range(0, 6):
        FROM = today - prev

        url = f"https://financialmodelingprep.com/api/v3/historical-chart/{PERIOD}/{SYMBOL}USD?from={FROM}&to={TO}&apikey={API_KEY}"
        print(url)

        response = get_jsonparsed_data(url)

        # print(response)

        f = open("crypto.csv", "a")

        for row in response:
            f.write(
                f"{row['date']},{row['open']},{row['high']},{row['low']},{row['close']},{row['volume']},{SYMBOL},{NAME}\n"
            )

        f.close()
        TO = FROM
        today = FROM
