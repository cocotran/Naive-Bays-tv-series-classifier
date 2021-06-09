from bs4.element import ResultSet
from bs4 import BeautifulSoup
from requests.models import Response
import csv
import requests


class Episode:
    def __init__(self, name: str, season: int, review_link: str, year: str) -> None:
        self.name = name
        self.season = season
        self.review_link = review_link
        self.year = year


def scrape(url: str, number_of_season: int) -> None:

    # Database
    raw_data: list = []

    def add_episode(name: str, season: int, review_link: str, year: str) -> None:
        raw_data.append(Episode(name, season, review_link, year))

    for season in range(1, number_of_season + 1):

        response: Response = requests.get(url + str(season))

        # Parse HTML
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        episode_list: ResultSet = soup.find_all("div", class_="info")

        for i in episode_list:
            name: str = i.a["title"]
            review_link: str = i.a["href"] + "reviews/?ref_=tt_ql_urv"
            year: str = i.find("div", class_="airdate").text.strip()[
                -4:
            ]  # Get last 4 character of date string: e.g. 24 Jun. 2015
            add_episode(name, season, review_link, year)

    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Name", "Season", "Review Link", "Year"])

        for i in range(len(raw_data)):
            episode: dict = raw_data[i]
            data: list = [
                i,
                episode.name,
                episode.season,
                episode.review_link,
                episode.year,
            ]
            writer.writerow(data)


if __name__ == "__main__":

    url: str = "https://www.imdb.com/title/tt4158110/episodes?season="
    scrape(url, 4)
