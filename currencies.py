import pandas as pd
from datetime import datetime
from data_utils import load_currencies_data

currencies_df = load_currencies_data()
currencies_df["date"] = pd.to_datetime(currencies_df["date"])


def get_price(price, currency, date):
    datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    iso_date = datetime_obj.date().isoformat()

    exchange = currencies_df[currencies_df["date"] == iso_date]

    return round(price * exchange[currency].values[0], 2)


def apply_prices(row, column, currency):
    row[column] = get_price(row[column], currency, row["date"])
    return row


def transform_price(df, column, currency):
    return df.apply(lambda row: apply_prices(row, column, currency), axis=1)
