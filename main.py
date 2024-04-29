from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from datetime import date
from pmdarima.arima import auto_arima
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('stock.csv')
stock_symbols = df['symbol'].unique()

app.layout = html.Div([
    html.H1('Stock Investor Portfolio'),
    html.Label('Select stock symbol(s):', style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id="stock-symbols-dropdown",
        options=stock_symbols,
        value=[],
        multi=True
    ),
    html.Label('Select date range:', style={'font-weight': 'bold'}),
    dcc.DatePickerRange(
        id='stock-market-date-range',
        min_date_allowed=date(2021, 9, 8),
        max_date_allowed=date(2024, 4, 25),
        initial_visible_month=date(2024, 4, 25),
        start_date=date(2023, 4, 25),
        end_date=date(2024, 4, 25)
    ),
    html.Div(id='output-container-start-date-picker-single'),
    dcc.Graph(id="plotly-express-x-graph"),
])


@app.callback(
    Output("plotly-express-x-graph", "figure"),
    Input("stock-symbols-dropdown", "value"),
    Input("stock-market-date-range", "start_date"),
    Input("stock-market-date-range", "end_date"),
)
def update_bar_chart(dims, start_date, end_date):
    df = pd.read_csv('stock.csv')

    df_filtered = df[df['symbol'].isin(dims) == True].sort_values(by=['date'], ascending=True)

    # train/test data splitting
    # train = df_filtered[(df_filtered['date'] >= "2021-09-08") & (df_filtered['date'] < "2023-12-30")]
    # test = df_filtered[(df_filtered['date'] > "2024-01-01")]

    # using arima model to predict data (średnia ruchoma)
    model = auto_arima(df_filtered['open'], seasonal=True, m=4)
    future_steps = 12  # np. prognoza na 12 miesięcy
    forecast, conf_int = model.predict(n_periods=future_steps, return_conf_int=True)

    print(forecast)

    fig = px.line(x=pd.date_range(start=df_filtered['date'], periods=future_steps, freq='M'), y=forecast)
    fig.show()

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
