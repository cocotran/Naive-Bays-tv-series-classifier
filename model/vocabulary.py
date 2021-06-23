from io import TextIOWrapper

import re

from collections import deque
from typing import Deque


file: TextIOWrapper = open("stopword.txt", "r")
stopwords: list = file.read().split("\n")
file.close()


number_of_positive_reviews: int = 0
number_of_negative_reviews: int = 0
training_positive_set: list = []
training_negative_set: list = []


clean_word = lambda word: re.sub(r"[^\w]", "", word)


file = open("training_positive.txt", "r")
training_positive_file_lines: list = file.read().split("\n")
file.close()

number_of_positive_reviews = len(training_positive_file_lines)

for line in training_positive_file_lines:
    for word in line.split(" "):
        training_positive_set.append(clean_word(word))


file = open("training_negative.txt", "r")
training_negative_file_lines: list = file.read().split("\n")
file.close()

number_of_negative_reviews = len(training_negative_file_lines)

for line in training_negative_file_lines:
    for word in line.split(" "):
        training_negative_set.append(clean_word(word))

vocabulary_set: list = list(set(training_positive_set + training_negative_set))

fm = open("model.txt", "w")
fr = open("remove.txt", "w")

for word in vocabulary_set:
    # Remove common unimportant words
    if word in stopwords:
        fr.write(word + "\n")
        vocabulary_set.remove(word)

vocabulary_set = deque(vocabulary_set)


def process(word: str, word_count: int, smoothing_delta: float) -> None:

    frequency_in_positive: int = 0
    frequency_in_negative: int = 0

    # Counting frequency in positive set
    for i in training_positive_set:
        if word == i:
            frequency_in_positive += 1

    # Counting frequency in positive set
    for i in training_negative_set:
        if word == i:
            frequency_in_negative += 1

    conditional_probability_in_positive: float = (
        frequency_in_positive + smoothing_delta
    ) / (len(training_positive_set) + len(vocabulary_set))
    conditional_probability_in_negative: float = (
        frequency_in_negative + smoothing_delta
    ) / (len(training_negative_set) + len(vocabulary_set))

    # Filtering words with low frequency
    if frequency_in_positive < 3 and frequency_in_negative < 3:
        fr.write(word + "\n")
        return

    fm.write("No." + str(word_count) + " " + word + "\n")
    fm.write(
        "{},{},{},{}\n".format(
            frequency_in_positive,
            conditional_probability_in_positive,
            frequency_in_negative,
            conditional_probability_in_negative,
        )
    )


def create_vocabulary(smoothing_delta: float) -> None:
    count = 0
    for word in vocabulary_set:
        process(word, count, smoothing_delta)
        count += 1
    fm.close()
    fr.close()


if __name__ == "__main__":
    create_vocabulary(1.0)
