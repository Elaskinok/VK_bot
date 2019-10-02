"""Parser of YandexMusic."""

import requests
from bs4 import BeautifulSoup

SOUNDS_BOX_CLASS = 'lightlist__cont'
SOUNDS_LIST_CLASS = 'd-track typo-track ' \
                    'd-track_selectable ' \
                    'd-track_with-cover ' \
                    'd-track_with-chart'

TRACK_NAME_CLASS = 'd-track__name'
TRACK_ARTIST_CLASS = 'deco-link deco-link_muted'

LINK_YANDEX_CHART = "https://music.yandex.by/chart"

PARSER_NAME = 'html.parser'


def get_html(link: str) -> str:
    """Return HTML file of page."""
    return requests.get(link).content.decode('utf-8', errors='ignore')


def get_track_data(track: BeautifulSoup) -> tuple:
    """Return name and artist's name of track."""
    track_name = track.find('div', {'class': TRACK_NAME_CLASS})\
        .get('title', '')
    track_artist = track.find('a', {'class': TRACK_ARTIST_CLASS})\
        .get('title', '')

    return track_name, track_artist


def get_track_list(link: str) -> dict:
    """Find and return class, with list of tracks."""
    soup = BeautifulSoup(get_html(link), PARSER_NAME)
    track_list = soup.find('div', {'class': SOUNDS_BOX_CLASS})
    return track_list.find_all('div', {'class': SOUNDS_LIST_CLASS})


def chart_as_string() -> str:
    """Parse HTML file and return chart list as string."""
    tracks = get_track_list(LINK_YANDEX_CHART)

    result = ''

    for index, track in enumerate(tracks, start=1):
        track_name, track_artist = get_track_data(track)

        result += f"{index}. {track_name} - {track_artist} \n"

    return result
