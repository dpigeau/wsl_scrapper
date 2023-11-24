from scrapper.website import Website
from scrapper.pages import ResultPage, HeatPage
from unittest import mock

@mock.patch.object(ResultPage, "parse")
@mock.patch.object(HeatPage, "parse")
@mock.patch("scrapper.website.utils")
def test_Website(mock_utils, mock_heatpage, mock_resultpage):
    website = Website()
    assert website.pages == []

    url = "mock_url"
    page1 = ResultPage(url)
    page2 = HeatPage(url)
    website.add_pages([page1, page2])
    assert website.pages == [page1, page2]

    mock_utils.build_path.return_value.exists.return_value = False
    website.scrap()
    assert mock_utils.write_json.call_count == 2


