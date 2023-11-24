import scrapper.utils as utils
from unittest import mock
import pytest
from pathlib import Path

@pytest.fixture
def folder_name():
    return "tests"

@pytest.fixture
def url():
    return "https://www.worldsurfleague.com/events/0000/ct/01/competition-name/results?roundId=00001"

@pytest.fixture
def file_path():
    return Path("data/tests/0000_ct_01_competition_name_results?roundId=00001.json")

@pytest.fixture
def heat_data():
    return [
        {
            "round_id": "21517",
            "heat_id": "92399",
            "athlete_id": "688",
            "athlete_name": "M. Pupo",
            "total_score": 12.5
        }
    ]

def test_build_path(url, folder_name, file_path):
    expect_path = utils.build_path(url, folder_name)
    assert file_path == expect_path

@mock.patch("scrapper.utils.json", autospec=True)
def test_write_json(mock_json, heat_data):

    file_path = mock.Mock()
    with mock.patch("builtins.open", mock.mock_open()) as m:
        utils.write_json(file_path, heat_data)
        file_path.parent.exists.assert_called_once()
        mock_json.dump.assert_called_once_with(heat_data, m(), indent=4)

def test_read_text():
    with mock.patch("builtins.open", mock.mock_open(read_data='one\ntwo')) as m:
        data = utils.read_txt("")
        assert data == ["one", "two"]
        

