from io import TextIOWrapper

import re

from collections import deque
from typing import Deque


file: TextIOWrapper = open("stopword.txt", "r")
stopwords: list = file.read().split("\n")
file.close()


training_positive_set: list = []
training_negative_set: list = []


clean_word = lambda word: re.sub(r"[^\w]", "", word)


file = open("training_positive.txt", "r")
training_positive_file_lines: list = file.read().split("\n")
file.close()

for line in training_positive_file_lines:
    for word in line.split(" "):
        training_positive_set.append(clean_word(word))


file = open("training_negative.txt", "r")
training_negative_file_lines: list = file.read().split("\n")
file.close()

for line in training_negative_file_lines:
    for word in line.split(" "):
        training_negative_set.append(clean_word(word))


visited_words: Deque = deque([])


def process(word: str, word_count: int) -> None:
    fm = open("model.txt", "a")
    fr = open("remove.txt", "a")

    frequency_in_positive: int = 0
    frequency_in_negative: int = 0

    # Only visit a word once
    if word in visited_words:
        return

    # Add new word to visited list
    visited_words.append(word)

    # Common unimportant words
    if word in stopwords:
        fr.write(word + "\n")
        return

    # Counting frequency in positive set
    for i in training_positive_set:
        if word == i:
            frequency_in_positive += 1

    # Counting frequency in positive set
    for i in training_negative_set:
        if word == i:
            frequency_in_negative += 1

    conditional_probability_in_positive: float = frequency_in_positive / len(
        training_positive_set
    )
    conditional_probability_in_negative: float = frequency_in_negative / len(
        training_negative_set
    )

    fm.write("No. " + str(word_count) + " " + word + "\n")
    fm.write(
        "{},{},{},{}\n".format(
            frequency_in_positive,
            conditional_probability_in_positive,
            frequency_in_negative,
            conditional_probability_in_negative,
        )
    )

    fm.close()
    fr.close()


if __name__ == "__main__":
    count = 0
    for word in training_positive_set:
        process(word, count)
        count += 1
