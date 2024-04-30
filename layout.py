from dash import dcc, html
from datetime import date
from data_utils import get_stock_symbols, get_crypto_symbols

# header
header = [
    html.Div([
        html.Div([
            html.Img(src='/assets/icon.svg', height='48px'),
            html.B('BUSINESS'),
            'dashboard'
        ], className='header__section'),
        html.Div([
            html.Div([
                'Currency:',
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
                    searchable=False,
                    style={"width": "100px", 'color': 'black'}
                )
            ], className='header__section'),

            html.Div([
                'Date range:',
                dcc.DatePickerRange(
                    id="stock-market-date-range",
                    minimum_nights=2,
                    min_date_allowed=date(2021, 9, 8),
                    max_date_allowed=date(2024, 4, 25),
                    initial_visible_month=date(2024, 4, 25),
                    start_date=date(2023, 4, 25),
                    end_date=date(2024, 4, 25),
                )
            ], className='header__section'),
        ], className='header__section'),
    ], className='header')
]

# Stock and summary container
stock_layout = [
    html.Div([
        html.Div([
            html.Div(["Stock Investor Portfolio"], className='container__title'),
            html.Div([
                html.Div([
                    html.Div(
                        [
                            html.Label("Select stock symbol(s):"),
                            dcc.Dropdown(
                                id="stock-symbols-dropdown",
                                options=get_stock_symbols(),
                                value=[],
                                multi=True,
                            ),
                        ],
                        style={"width": "50%"},
                    ),
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
                ], className='container__filters'),

                dcc.Graph(id="stock-graph"),
            ], className='container__content')

        ], className='container', style={'width': '70%'}),

        html.Div([
            dcc.Graph(id="stock-gauge-7", style={"width": "100%", 'height': '300px', 'margin-top': '-50px'},
                      config={'displayModeBar': False}),
            dcc.Graph(
                id="stock-gauge-15", style={"width": "100%", 'height': '300px', 'margin-top': '-80px'},
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id="stock-gauge-30", style={"width": "100%", 'height': '300px', 'margin-top': '-80px'},
                config={'displayModeBar': False}
            ),
        ], className='container', style={'width': '30%'}),
    ], style={'display': 'flex', 'gap': '40px'})
]

# currencies container
currencies_layout = [
    html.Div([
        html.Div(["Currencies"], className='container__title'),
        html.Div([
            dcc.Graph(id="currency-graph"),
        ], className='container__content'),
    ], className='container'),
]

# cryptocurrencies container
cryptocurrencies_layout = [
    html.Div([
        html.Div(["Cryptocurrencies"], className='container__title'),
        html.Div([
            html.Div([
                html.Div(
                    [
                        html.Label("Select crypto symbol(s):"),
                        dcc.Dropdown(
                            id="crypto-currency-dropdown",
                            options=get_crypto_symbols(),
                            value=[],
                            multi=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Div(
                    [
                        html.Label("Select type of data:"),
                        dcc.Dropdown(
                            id="crypto-data-dropdown",
                            options=["open", "high", "low", "close", "volume"],
                            value="open",
                            multi=False,
                            clearable=False,
                        ),
                    ]
                ),
            ], className='container__filters'),

            dcc.Graph(id="crypto-graph"),
        ], className='container__content'),
    ], className='container')
]
