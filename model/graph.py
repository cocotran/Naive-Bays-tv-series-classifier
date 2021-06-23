from io import TextIOWrapper
import matplotlib.pyplot as plt
import numpy as np

smoothing_delta: list = []
correctness_percentage: list = []

file: TextIOWrapper = open("smooth-graph.txt", "r")

for line in file:
    data: list = line.replace("\n", "").split(",")
    smoothing_delta.append(float(data[0]))
    correctness_percentage.append(float(data[1]))

if __name__ == "__main__":
    plt.plot(smoothing_delta, correctness_percentage)
    # plt.show()
    plt.savefig("graph.png")
