from bs4 import BeautifulSoup
from bs4.element import ResultSet

import requests
from requests.models import Response

import csv


class Episode:
    def __init__(self, name: str, season: int, review_link: str, year: str) -> None:
        self.name = name
        self.season = season
        self.review_link = review_link
        self.year = year


def scrape(url: str, number_of_season: int) -> None:

    # Temporary database
    raw_data: list = []

    def add_episode_to_database(
        name: str, season: int, review_link: str, year: str
    ) -> None:
        raw_data.append(Episode(name, season, review_link, year))

    # Scrape data of each episode
    for season in range(1, number_of_season + 1):

        response: Response = requests.get(url + str(season))

        # Parse HTML
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        episode_list: ResultSet = soup.find_all(
            "div", class_="info"
        )  # All info of an episode is contained in a div with attribute class="info"

        # Add episode info to temporary database
        for i in episode_list:
            name: str = i.a["title"]
            review_link: str = (
                "https://www.imdb.com/" + i.a["href"] + "reviews/?ref_=tt_ql_urv"
            )  # All user review page has a common path ending
            year: str = i.find("div", class_="airdate").text.strip()[
                -4:
            ]  # Get last 4 character of date string: e.g. 24 Jun. 2015
            add_episode_to_database(name, season, review_link, year)

    # Convert temporary database to CSV file
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


class Review:
    def __init__(self, rating: int, title: str, content: str) -> None:
        self.rating = rating
        self.title = title
        self.content = content


def classify() -> None:
    positive_reviews: list = []
    negative_reviews: list = []

    def add_review_to_database(review: Review) -> None:
        if review.rating != None:
            if review.rating >= 8:
                positive_reviews.append(review)
            else:
                negative_reviews.append(review)

    with open("data.csv", "r", newline="") as file:
        reader = csv.reader(file)
        # skip header
        next(reader)
        for row in reader:

            response: Response = requests.get(row[3])

            # Parse HTML
            soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

            review_list: ResultSet = soup.find_all("div", class_="review-container")

            for i in review_list:
                rating_tag = i.find("span").find("span")
                rating: int = int(rating_tag.text) if rating_tag != None else None
                title: str = i.find("a", class_="title").text.lower()
                content: str = i.find("div", class_="text").text.lower()
                add_review_to_database(Review(rating, title, content))

    training_positive_set = open("training_positive.txt", "w")
    training_negative_set = open("training_negative.txt", "w")
    testing_positive = open("testing_positive.txt", "w")
    testing_negative = open("testing_negative.txt", "w")

    positive_set_midpoint: int = int(len(positive_reviews) / 2)
    negative_set_midpoint: int = int(len(negative_reviews) / 2)

    for i in range(positive_set_midpoint):
        training_positive_set.write(
            positive_reviews[i].title + " " + positive_reviews[i].content
        )

    for i in range(positive_set_midpoint, len(positive_reviews)):
        testing_positive.write(
            positive_reviews[i].title + " " + positive_reviews[i].content
        )

    for i in range(negative_set_midpoint):
        training_negative_set.write(
            negative_reviews[i].title + " " + negative_reviews[i].content
        )

    for i in range(negative_set_midpoint, len(negative_reviews)):
        testing_negative.write(
            negative_reviews[i].title + " " + negative_reviews[i].content
        )

    training_positive_set.close()
    training_negative_set.close()
    testing_positive.close()
    testing_negative.close()


if __name__ == "__main__":

    url: str = "https://www.imdb.com/title/tt4158110/episodes?season="
    scrape(url, 4)
    classify()
