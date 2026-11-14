from pathlib import Path
from datetime import datetime

import pandas as pd
import pytest

from tenniscareer.download import _format_player_name
from tenniscareer.clean_date import _clean_data, _extract_rows, _opponent_age


def _load_test_rows(filename):
    path = Path(__file__).parent / "data" / filename
    return _extract_rows(path.read_text(encoding="utf-8"))


def test_name_forms():
    names = ["serena williams", "Serena Williams", "SerenaWilliams"]
    for name in names:
        assert _format_player_name(name) == "SerenaWilliams"


def test_female_birthdates():
    rows = _load_test_rows("FemalePlayerCareer.JS")
    data = _clean_data(rows, "1981-09-26")

    event_date = datetime.strptime(rows[0][0], "%Y%m%d")
    player_dob = datetime(1981, 9, 26)
    opponent_dob = datetime.strptime(rows[0][16], "%Y%m%d")

    expected_player_age = (event_date - player_dob).days / 365.25
    expected_opponent_age = (event_date - opponent_dob).days / 365.25
    expected_age_diff = (opponent_dob - player_dob).days / 365.25

    assert len(rows) == 3
    assert len(data) == len(rows)
    assert data.loc[0, "player_age"] == pytest.approx(expected_player_age)
    assert data.loc[0, "opponent_age"] == pytest.approx(expected_opponent_age)
    assert data.loc[0, "age_diff"] == pytest.approx(expected_age_diff)


def test_male_numeric_ages():
    rows = _load_test_rows("MalePlayerCareer.JS")

    event_date = pd.to_datetime(rows[0][0], format="%Y%m%d")

    expected_age = float(rows[0][16])
    actual_age = _opponent_age(rows[0][16], event_date)

    assert len(rows) == 3
    assert actual_age == pytest.approx(expected_age)


def test_invalid_date_is_removed():
    rows = _load_test_rows("FemalePlayerCareer.JS")
    original_count = len(rows)

    rows[1][0] = "invalid-date"
    data = _clean_data(rows, "1981-09-26")

    assert len(data) == original_count - 1
    assert data["date"].notna().all()


def test_missing_opponent_age():
    age = _opponent_age("", pd.Timestamp("1995-10-30"))
    assert pd.isna(age)


def test_invalid_source():
    with pytest.raises(ValueError):
        _extract_rows("var unrelated = [];")


def test_empty_name():
    with pytest.raises(ValueError):
        _format_player_name("")