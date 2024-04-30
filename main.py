from dash import Dash, html, Input, Output
import plotly.express as px
from utils import generate_proper_gauge
from layout import header, stock_layout, currencies_layout, cryptocurrencies_layout
from data_utils import load_stock_data, load_currencies_data, load_crypto_data, get_data_in_time_range, \
    get_data_by_symbols, get_data_by_currencies

app = Dash(__name__)

app.layout = html.Div(
    [
        *header,
        *stock_layout,
        *currencies_layout,
        *cryptocurrencies_layout
    ],
    className='dashboard-container'
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
    df = load_stock_data()
    df_prepared = get_data_by_symbols(df, symbols)
    df_prepared = get_data_in_time_range(df_prepared, start_date, end_date)

    fig = px.line(df_prepared, x="date", y=type_of_data, color="symbol", template="simple_white")
    fig.update_yaxes(showgrid=True)
    fig.update_xaxes(rangeslider_visible=True)

    return fig


@app.callback(
    Output("stock-gauge-15", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "end_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_15(symbols, end_date, type_of_data, currency):
    days_back = 15
    df = load_stock_data()
    return generate_proper_gauge(df, symbols, end_date, type_of_data, days_back, currency)


@app.callback(
    Output("stock-gauge-7", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "end_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_7(symbols, end_date, type_of_data, currency):
    days_back = 7
    df = load_stock_data()
    return generate_proper_gauge(df, symbols, end_date, type_of_data, days_back, currency)


@app.callback(
    Output("stock-gauge-30", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "end_date"),
    Input("stock-data-dropdown", "value"),
    Input("stock-currency-dropdown", "value"),
)
def update_stock_gauge_30(symbols, end_date, type_of_data, currency):
    days_back = 30
    df = load_stock_data()
    return generate_proper_gauge(df, symbols, end_date, type_of_data, days_back, currency)


@app.callback(
    Output("currency-graph", "figure"),
    Input("stock-currency-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-market-date-range", "end_date"),
)
def update_currency_data(currency, start_date, end_date):
    df = load_currencies_data()

    if currency:
        df_prepared = get_data_by_currencies(df, currency)
        df_prepared = get_data_in_time_range(df_prepared, start_date, end_date)

        fig = px.line(df_prepared, x="date", y=currency, template='simple_white')
        fig.update_yaxes(showgrid=True)
        fig.update_xaxes(rangeslider_visible=True)
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
    df = load_crypto_data()
    df_prepared = get_data_by_symbols(df, symbols)
    df_prepared = get_data_in_time_range(df_prepared, start_date, end_date)

    fig = px.line(df_prepared, x="date", y=type_of_data, color="symbol", template='simple_white')
    fig.update_yaxes(showgrid=True)
    fig.update_xaxes(rangeslider_visible=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
