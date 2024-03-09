"""Generates a file with random integers and saves them to a file called random_integers.txt."""

import os
import random
import sys

from tqdm import tqdm


def create_x_file(n: int = 100, max_num: int = sys.maxsize) -> None:
    """
    Generates n random integers and saves them to a file called random_integers.txt.

    Args:
      n: The number of random integers to generate.
      max_num: The maximum value for the random integers.
    """

    n = int(input("Number of random integers to generate: "))  # Default value is 100

    random_integers = [random.randint(1, max_num) for _ in tqdm(range(n))]

    with open(os.path.join("data", "random_integers.txt"), "w", encoding="utf-8") as f:
        for integer in random_integers:
            f.write(str(integer) + "\n")

    print(f"{n} random integers have been generated and saved to random_integers.txt")


if __name__ == "__main__":
    create_x_file(100, sys.maxsize)
