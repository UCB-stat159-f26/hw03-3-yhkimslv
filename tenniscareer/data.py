from .download import (_download_career, _format_player_name, _get_player_dob,)

from .clean_date import _extract_rows, _clean_data


def get_career_data(player_name):
    player = _format_player_name(player_name)
    text = _download_career(player)
    player_dob = _get_player_dob(player)
    data = _clean_data(_extract_rows(text), player_dob)
    data.attrs["player_name"] = player_name.strip()
    return data