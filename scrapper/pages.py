import abc
from typing import Dict, List
import re
from bs4 import BeautifulSoup
import requests
import json

class Page(abc.ABC):
    url: str
    _soup: BeautifulSoup = None

    def __init__(self, url):
        self.url = url
        
    @property
    def soup(self) -> BeautifulSoup:
        html_text = requests.get(self.url).text
        self._soup = BeautifulSoup(html_text, 'html.parser')
        return self._soup

    def parse(self) -> List[Dict]:
        ...

class ResultPage(Page):
    url: str

    def __init__(self, url: str):
        super().__init__(url)

    def parse(self) -> List[Dict]:
        """ Returns all the raw heat results """
        
        pattern = "(Watch (Opening Round|Elimination Round|Round of 16|Qualifying Round|Night Session|Quarterfinals|Semifinals|Final)( - Heat [0-9]|[1-9][0-9])?)"
        regex = re.compile(pattern)
        tags = self.soup.find_all("a", title = regex)
        return [json.loads(t.attrs["data-gtm-event"]) for t in tags]

class HeatPage(Page):
    url: str

    def __init__(self, url: str):
        super().__init__(url)

    def parse(self) -> List[Dict]:
        """ Returns the total heat scores """

        def score_to_float(score: str) -> float:
            """"""
            try:
                return float(score)
            except ValueError:
                return 0.0
        
        # get round id from url
        round_id = re.findall(r"roundId=([0-9]{5})$", self.url)[0]
        
        # get heat and athlete ids
        pattern_ids = "hot-heat-athlete--([0-9]{5})-([0-9]{3,4})"
        regex_ids = re.compile(pattern_ids)
        heat_tags = self.soup.find_all("div", id=regex_ids)
        heat_ids = re.findall(pattern_ids, str(heat_tags))

        print(heat_ids)

        # get athlete short names
        athlete_names_tags = self.soup("div", class_="hot-heat-athlete__name hot-heat-athlete__name--short")
        athlete_names = [t.contents[0] for t in athlete_names_tags if t.contents[0][:6]!="Seed #"] # add if statement for Surf Ranch Pro

        print(athlete_names)

        # get total scores
        pattern_scores = "(hot-heat-athlete__score)|(wavepool-hybrid__total hot-heat__wave-results-cell)"
        regex_scores = re.compile(pattern_scores)
        total_scores_tags = self.soup("div", class_=regex_scores)
        total_scores = [t.contents[0] for t in total_scores_tags if t.contents[0]!="Total"] # add if statement for Surf Ranch Pro

        print(total_scores)
        
        # append to list
        scores = list()
        for i in range(len(heat_ids)):
            score = {
                "round_id": round_id,
                "heat_id": heat_ids[i][0],
                "athlete_id": heat_ids[i][1],
                "athlete_name": athlete_names[i],
                "total_score": score_to_float(total_scores[i])
            }
            scores.append(score)

        return scores
    