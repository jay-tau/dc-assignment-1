"""
Splits a text file into n separate text files, based on the number of lines.

This script is useful for splitting large text files into smaller chunks to enable
parallel processing.

Usage:
  - Run the script and input the number of files to split the text file into.
  - The output files will be created in the same directory as the input file.
  - The output files will be named as "{file_name}_{n}_{file_index}.txt".

Example:
  - Input: "master_file.txt" with 1000 lines and n = 5.
  - Output: 5 files named "master_file_5_0.txt", "master_file_5_1.txt", ...,
            "master_file_5_4.txt" with 200 lines each.

Note:
  - The original file will not be modified.
  - The output files will be created in the same directory as the input file.
  - The output files will be named as "{file_name}_{n}_{file_index}.txt".
  - The original file is assumed to be encoded in UTF-8.

Raises:
  - ValueError: If the number of lines in the file is not divisible by n.
"""

import os

from tqdm import tqdm


def split_file(file_name: str, n: int) -> None:
    """
    Splits a text file into n separate text files, based on the number of lines.

    Args:
      file_name: The name of the text file to split.
      n: The number of files to split the text file into.

    Raises:
      ValueError: If the number of lines in the file is not divisible by n.
    """

    # Read the total number of lines in the file
    with open(file_name, encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)

    # Check if the number of lines is divisible by n
    if total_lines % n != 0:
        raise ValueError("Number of lines is not divisible by n")

    # Calculate the number of lines per file
    lines_per_file = total_lines // n

    # Open the original file and create output files
    with open(file_name, encoding="utf-8") as f:
        for i, line in tqdm(enumerate(f)):
            # Calculate the index of the output file
            file_index = i // lines_per_file

            # Open the output file (create if it doesn't exist) with explicit encoding
            with open(
                f"{file_name[:-4]}_{n}_{file_index}.txt", "a", encoding="utf-8"
            ) as output_file:
                output_file.write(line)


if __name__ == "__main__":
    # Get the filename and number of files from the user
    filename = os.path.join("..", "data", "master_file.txt")
    n_chunks: int = int(input("Enter the number of files to split into: "))

    print(f"{n_chunks}:", end="\n")

    split_file(filename, n_chunks)

    print(f"File '{filename}' successfully split into {n_chunks} files.")
    print("DONE")
