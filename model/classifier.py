from io import TextIOWrapper
from collections import deque
from typing import Deque
from math import log10


vocabulary_list: Deque = deque([])
probability_list: Deque = deque([])

file: TextIOWrapper = open("model.txt", "r")
for line in file:
    line = line.replace("\n", "")
    if "No." in line:
        vocabulary_list.append(line.split(" ")[1])
    else:
        probability_list.append(line.split(","))


def classify(review_number: int, review: str, correct_result: str) -> bool:
    review_words: list = review.split(" ")

    p_positive: float = 0.5
    p_negative: float = 0.5

    for word in review_words:
        if word in vocabulary_list:
            index: int = vocabulary_list.index(word)
            p_positive *= log10(float(probability_list[index][1]))
            p_negative *= log10(float(probability_list[index][3]))

    if p_positive + p_negative == 0.0:
        print(review_number)
        return False

    p_review_positive: float = p_positive / (p_positive + p_negative)
    p_review_negative: float = p_negative / (p_positive + p_negative)
    result: str = "positive" if p_review_positive >= p_review_negative else "negative"
    compare: str = "right" if result == correct_result else "wrong"

    file: TextIOWrapper = open("result.txt", "a")
    file.write("No." + str(review_number) + " " + review[:20] + "\n")
    file.write(
        "{},{},{},{},{}\n".format(
            p_review_positive, p_review_negative, result, correct_result, compare
        )
    )
    file.close()

    return compare == "right"


if __name__ == "__main__":
    file: TextIOWrapper = open("testing_positive.txt", "r")
    test_set: list = file.read().split("\n")
    file.close()

    count: int = 0
    correct_count: int = 0

    for test in test_set:
        if classify(count, test, "positive"):
            correct_count += 1
        count += 1

    file: TextIOWrapper = open("testing_negative.txt", "r")
    test_set: list = file.read().split("\n")
    file.close()

    for test in test_set:
        if classify(count, test, "negative"):
            correct_count += 1
        count += 1

    file: TextIOWrapper = open("result.txt", "a")
    file.write(
        "The prediction correctness is {}%".format((correct_count * 100) / count)
    )
    file.close()
