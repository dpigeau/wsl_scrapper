from scrapper.website import Website
from scrapper.pages import ResultPage, HeatPage
import scrapper.utils as utils
import logging

logging.getLogger().setLevel(logging.INFO)

if __name__=="__main__":

    urls_file_path = "wsl_scrapper/urls.txt"
    urls = utils.read_txt(urls_file_path)

    pages = []
    for url in urls:
        pages.append(ResultPage(url))
        pages.append(HeatPage(url))

    website = Website()
    website.add_pages(pages)
    website.scrap()
    