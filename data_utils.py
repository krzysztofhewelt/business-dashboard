import pandas as pd


def load_stock_data():
    return pd.read_csv('stock/stock.csv')


def load_currencies_data():
    return pd.read_csv('exchange/currencies.csv')


def load_crypto_data():
    return pd.read_csv('stock/crypto.csv')


def get_stock_symbols():
    stock_data = load_stock_data()
    return stock_data['symbol'].unique()


def get_crypto_symbols():
    crypto_data = load_crypto_data()
    return crypto_data['symbol'].unique()


def get_data_in_time_range(df, start_date, end_date):
    return df[(df["date"] >= start_date) & (df["date"] <= end_date)]


def get_data_by_symbols(df, symbols):
    return df[df["symbol"].isin(symbols) == True].sort_values(by=["date"], ascending=True)


def get_data_by_currencies(df, currency):
    return df[["date", currency]].sort_values(by=["date"], ascending=True)
