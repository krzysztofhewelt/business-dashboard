import plotly.graph_objects as go
import pandas as pd


def get_values(data, target_date, days_back, type_of_data):
    """
    Get values for a given date and a past date, and calculate maximum and minimum values.

    Parameters:
        data (DataFrame): DataFrame containing 'date' and 'open' columns.
        target_date (str): Date for which values are to be retrieved.
        days_back (int): Number of days to go back for the past date.

    Returns:
        tuple: A tuple containing the following values:
            - Value for the given date
            - Value for the past date
            - Maximum value between given and past date
            - Minimum value between given and past date
    """
    # Convert date column to datetime type

    data["date"] = pd.to_datetime(data["date"])

    # Convert target_date to datetime
    target_date = pd.to_datetime(target_date)

    # Calculate past date
    past_date = target_date - pd.Timedelta(days=days_back)

    # Filter rows for the target date and past date
    target_row = data[data["date"].dt.date == target_date.date()]
    past_row = data[data["date"].dt.date == past_date.date()]

    # Get values for target date and past date
    target_value = target_row[type_of_data].values[0] if not target_row.empty else 0
    past_value = past_row[type_of_data].values[0] if not past_row.empty else 0

    # Calculate maximum and minimum values
    max_value = (
        max(target_value, past_value)
        if target_value is not None and past_value is not None
        else 0
    )
    min_value = (
        min(target_value, past_value)
        if target_value is not None and past_value is not None
        else 0
    )

    return target_value, past_value, max_value, min_value


def generate_proper_gauge(data, symbols, end_date, type_of_data, days_back, currency):
    if not symbols:
        return get_gauge(0, 0, 0, 0, days_back)

    df_filtered = data[data["symbol"] == symbols[0]]

    value, past_value, max_value, min_value = get_values(
        data=df_filtered.copy(),
        target_date=end_date,
        days_back=days_back,
        type_of_data=type_of_data,
    )

    return get_gauge(value, past_value, min_value, max_value, days_back)


def get_gauge(value, past_value, min_value, max_value, days):
    return go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=value,
            mode="delta",
            title={"text": f"Last {days} days"},
            delta={"reference": past_value},
            gauge={
                "axis": {"range": [min_value, max_value]},
                "steps": [
                    {"range": [min_value, max_value], "color": "lightgray"},
                ],
            },
        )
    )
