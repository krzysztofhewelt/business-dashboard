from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from datetime import date
import pandas as pd
from utils import get_gauge, get_values

app = Dash(__name__)

df_stock = pd.read_csv("stock/stock.csv")
stock_symbols = df_stock["symbol"].unique()

df_crypto = pd.read_csv("stock/crypto.csv")
crypto_symbol = df_crypto["symbol"].unique()

app.layout = html.Div(
    [
        html.H1("Stock Investor Portfolio"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select stock symbol(s):"),
                        dcc.Dropdown(
                            id="stock-symbols-dropdown",
                            options=stock_symbols,
                            value=[],
                            multi=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Div(
                    [
                        html.Label("Select date range:"),
                        dcc.DatePickerRange(
                            id="stock-market-date-range",
                            min_date_allowed=date(2021, 9, 8),
                            max_date_allowed=date(2024, 4, 25),
                            initial_visible_month=date(2024, 4, 25),
                            start_date=date(2023, 4, 25),
                            end_date=date(2024, 4, 25),
                        ),
                        html.Div(id="output-container-start-date-picker-single"),
                    ]
                ),
            ],
            style={"display": "flex", "gap": "40px", "width": "100%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select type of data:"),
                        dcc.Dropdown(
                            id="stock-data-dropdown",
                            options=["open", "high", "low", "close", "volume"],
                            value="open",
                            multi=False,
                            clearable=False,
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label(
                            "Select currency:", htmlFor="stock-currency-dropdown"
                        ),
                        dcc.Dropdown(
                            id="stock-currency-dropdown",
                            options=[
                                "PLN",
                                "EUR",
                                "USD",
                                "GBP",
                                "SEK",
                                "NOK",
                                "CHF",
                                "JPY",
                            ],
                            value="USD",
                            multi=False,
                            clearable=False,
                        ),
                    ]
                ),
            ],
            style={"display": "flex", "gap": "40px", "width": "100%"},
        ),
        html.Div(
            [
                dcc.Graph(id="stock-graph", style={"width": "100%", "height": "100%"}),
            ],
            style={"display": "flex"},
        ),
        html.Div(
            [
                dcc.Graph(id="stock-gauge-7", style={"width": "33%", "height": "100%"}),
                dcc.Graph(
                    id="stock-gauge-15", style={"width": "33%", "height": "100%"}
                ),
                dcc.Graph(
                    id="stock-gauge-30", style={"width": "33%", "height": "100%"}
                ),
            ],
            style={"display": "flex"},
        ),
        html.H1("Currencies"),
        dcc.Graph(id="currency-graph", style={"width": "80%", "height": "100%"}),
        html.H1("Cryptocurrencies"),
        html.Label("Select cryptocurrencies:"),
        dcc.Dropdown(
            id="crypto-currency-dropdown", options=crypto_symbol, value=[], multi=True
        ),
        html.Label("Select type of data:"),
        dcc.Dropdown(
            id="crypto-data-dropdown",
            options=["open", "high", "low", "close", "volume"],
            value="open",
            multi=False,
            clearable=False,
        ),
        dcc.Graph(id="crypto-graph"),
    ],
    style={"padding": "20px 30px"},
)


@app.callback(
    Output("stock-graph", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-market-date-range", "end_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_data(symbols, start_date, end_date, type_of_data, currency):
    df = pd.read_csv("stock/stock.csv")

    df_filtered = df[df["symbol"].isin(symbols) == True].sort_values(
        by=["date"], ascending=True
    )
    df_filtered = df_filtered[
        (df_filtered["date"] >= start_date) & (df_filtered["date"] <= end_date)
    ]

    fig = px.line(df_filtered, x="date", y=type_of_data, color="symbol")
    fig.update_xaxes(rangeslider_visible=True)

    return fig


@app.callback(
    Output("stock-gauge-15", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_15(symbols, start_date, type_of_data, currency):
    df_filtered = df_stock[df_stock["symbol"] == symbols[0]]
    days_back = 15

    value, past_value, max_value, min_value = get_values(
        data=df_filtered,
        target_date=start_date,
        days_back=days_back,
        type_of_data=type_of_data,
    )

    return get_gauge(value, past_value, min_value, max_value, days_back)

@app.callback(
    Output("stock-gauge-7", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_7(symbols, start_date, type_of_data, currency):
    df_filtered = df_stock[df_stock["symbol"] == symbols[0]]
    days_back = 7

    value, past_value, max_value, min_value = get_values(
        data=df_filtered,
        target_date=start_date,
        days_back=days_back,
        type_of_data=type_of_data,
    )

    return get_gauge(value, past_value, min_value, max_value, days_back)

@app.callback(
    Output("stock-gauge-30", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_30(symbols, start_date, type_of_data, currency):
    df_filtered = df_stock[df_stock["symbol"] == symbols[0]]
    days_back = 30

    value, past_value, max_value, min_value = get_values(
        data=df_filtered,
        target_date=start_date,
        days_back=days_back,
        type_of_data=type_of_data,
    )

    return get_gauge(value, past_value, min_value, max_value, days_back)


@app.callback(
    Output("currency-graph", "figure"),
    Input("stock-currency-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-market-date-range", "end_date"),
)
def update_currency_data(currency, start_date, end_date):
    df = pd.read_csv("exchange/currencies.csv")

    if currency:
        df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        df_filtered = df_filtered[["date", currency]]
        fig = px.line(df_filtered, x="date", y=currency)
        return fig

    return None


@app.callback(
    Output("crypto-graph", "figure"),
    Input("crypto-currency-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-market-date-range", "end_date"),
    Input("crypto-data-dropdown", "value"),
)
def update_crypto_data(symbols, start_date, end_date, type_of_data):
    df = pd.read_csv("stock/crypto.csv")

    df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df_filtered = df_filtered[df_filtered["symbol"].isin(symbols) == True].sort_values(
        by=["date"], ascending=True
    )
    fig = px.line(df_filtered, x="date", y=type_of_data, color="symbol")
    fig.update_xaxes(rangeslider_visible=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
