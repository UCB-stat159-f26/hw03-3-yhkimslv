import re

from urllib.error import HTTPError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

import pandas as pd


BASE_URL = "https://www.tennisabstract.com"


def _format_player_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Enter a nonempty player name.")
    formatted = ""
    for word in name.split():
        if word.islower() or word.isupper():
            word = word.capitalize()
        formatted += word
    return formatted


def _download_text(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except HTTPError as error:
        if error.code == 404:
            raise ValueError("Player not found. Check the name.") from error
        raise RuntimeError(f"Tennis Abstract returned HTTP {error.code}.") from error


def _extract_dob(text):
    match = re.search(r"""\bvar\s+dob\s*=\s*["']?(\d{8})""", text)
    if match is None:
        raise ValueError("Player date of birth not found.")
    return pd.to_datetime(match.group(1), format="%Y%m%d")


def _get_player_dob(player):
    path = "/cgi-bin/wplayer-classic.cgi"
    url = f"{BASE_URL}{path}?p={quote(player)}&f=ACareerqq"
    page = _download_text(url)
    pattern = r"""<script\b[^>]*\bsrc\s*=\s*["']([^"']+)["']"""
    source = page
    scripts = re.findall(pattern, page, re.I)
    for script in scripts:
        if script.endswith("/" + player + ".js"):
            source += "\n" + _download_text(urljoin(url, script))
    return _extract_dob(source)


def _download_career(player):
    url = f"{BASE_URL}/jsmatches/{quote(player)}Career.js"
    return _download_text(url)