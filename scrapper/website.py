
from scrapper.pages import Page, ResultPage, HeatPage
from typing import List 
import scrapper.utils as utils
import logging

class Website:
    pages: List[Page]

    def __init__(self) -> None:
        self.pages = []
    
    def add_pages(self, pages: List[Page]) -> None:
        self.pages.extend(pages)

    def scrap(self) -> None:
        """ """
        
        for page in self.pages:

            print(type(page))
            
            match page:
                case ResultPage():
                    target_folder = "raw_results"
                case HeatPage():
                    target_folder = "raw_heats"
            
            file_path = utils.build_path(page.url, target_folder)

            if file_path.exists():
                logging.info(f"File exists already. URL won't be scrapped: {page.url}")
            else:
                heats = page.parse() 
                utils.write_json(file_path, heats)
                logging.info(f"New file created under {file_path}")