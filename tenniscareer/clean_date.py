import pandas as pd


def _extract_rows(text):
    rows = []

    for line in text.splitlines():
        values = line.split('"')[1::2]
        if len(values) > 16 and len(values[0]) == 8 and values[0].isdigit():
            rows.append(values)

    if not rows:
        raise ValueError("No career match data found.")

    return rows


def _opponent_age(value, event_date):
    value = str(value).strip()
    if len(value) == 8 and value.isdigit():
        dob = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        return (event_date - dob).days / 365.25

    return pd.to_numeric(value, errors="coerce")


def _clean_data(rows, player_dob):
    data = pd.DataFrame(rows).drop_duplicates()[[0, 4, 11, 16]].copy()
    data.columns = ["date", "result", "opponent", "opponent_age_raw"]

    data["player_age"] = (data["date"] - pd.Timestamp(player_dob)).dt.days / 365.25

    pairs = zip(data["opponent_age_raw"], data["date"])
    data["opponent_age"] = [_opponent_age(value, date) for value, date in pairs]

    data["age_diff"] = data["player_age"] - data["opponent_age"]

    data = data.drop(columns="opponent_age_raw").dropna()

    return data.reset_index(drop=True)