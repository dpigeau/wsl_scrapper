from scrapper.pages import Page, ResultPage, HeatPage
import pytest
from unittest import mock
from bs4 import BeautifulSoup

@pytest.fixture
def html():
    return """
       <html>
        <a title='Watch Opening Round - Heat 1' data-gtm-event='{"heat-1":1}'> Replay </a>
        <a title='Watch Elimination Round - Heat 2' data-gtm-event='{"heat-2":2}'> Replay </a>
        <a title='Watch Round of 16 - Heat 3' data-gtm-event='{"heat-3":3}'> Replay </a>
        <a title='Watch Qualifying Round - Heat 4' data-gtm-event='{"heat-4":4}'> Replay </a>
        <a title='Watch Night Session - Heat 5' data-gtm-event='{"heat-5":5}'> Replay </a>
        <a title='Watch Quarterfinals - Heat 6' data-gtm-event='{"heat-6":6}'> Replay </a>
        <a title='Watch Semifinals - Heat 7' data-gtm-event='{"heat-7":7}'> Replay </a>
        <a title='Watch Final' data-gtm-event='{"heat-8":8}'> Replay </a>

        <div class='hot-heat-athlete__name hot-heat-athlete__name--short'>Seed #1</div>
        <div class='hot-heat-athlete__score'>Total</div>
        <div id='hot-heat-athlete--11111-111'>
            <div class='hot-heat-athlete__name hot-heat-athlete__name--short'>J.Flores</div>
            <div class='hot-heat-athlete__score'>1.00</div>
        </div>

        <div id='hot-heat-athlete--22222-222'>
            <div class='hot-heat-athlete__name hot-heat-athlete__name--short'>J.Smith</div>
            <div class='wavepool-hybrid__total hot-heat__wave-results-cell'>not_a_float</div>
        </div>

        </html>
    """

@pytest.fixture
def parse_results():
    return [
        {"heat-1":1},
        {"heat-2":2},
        {"heat-3":3},
        {"heat-4":4},
        {"heat-5":5},
        {"heat-6":6},
        {"heat-7":7},
        {"heat-8":8},   
    ]

@pytest.fixture
def parse_heats():
    return [
        {
            "round_id": "12345",
            "heat_id": "11111",
            "athlete_id": "111",
            "athlete_name": "J.Flores",
            "total_score":1.00,
        },
        {
            "round_id": "12345",
            "heat_id": "22222",
            "athlete_id": "222",
            "athlete_name": "J.Smith",
            "total_score": 0.00,
        }
    ]

@mock.patch("scrapper.pages.requests")
def test_Page(mock_requests, html):
    url = "mock_url"
    mock_requests.get.return_value.text = html
    page = Page(url)
    assert page.url == url
    assert page.soup == BeautifulSoup(html, "html.parser")

@mock.patch("scrapper.pages.requests")
def test_ResultPage(mock_requests, html, parse_results):
    url = "mock_url"
    mock_requests.get.return_value.text = html
    page = ResultPage(url)
    assert page.url == url
    assert page.soup == BeautifulSoup(html, "html.parser")
    assert page.parse() == parse_results

@mock.patch("scrapper.pages.requests")
def test_HeatPage(mock_requests, html, parse_heats):
    url = "mock_url/roundId=12345"
    mock_requests.get.return_value.text = html
    page = HeatPage(url)
    assert page.url == url
    assert page.soup == BeautifulSoup(html, "html.parser")
    assert page.parse() == parse_heats
