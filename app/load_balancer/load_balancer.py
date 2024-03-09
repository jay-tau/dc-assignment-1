"""
This script sends requests to the searchers and writes the response data to a csv file.

Data is read from `data/random_integers.txt` and response is written to `data/response_data.csv`
Script takes the number of chunks as an environment variable NUM_CHUNKS and sends requests to the searchers based on the number of chunks.
The chunk ranges are defined in the CHUNK_RANGES dictionary.
The script sends requests to the searchers based on the chunk range of the number x and the number of chunks.
The response data is a 4-tuple of (n_chunks, x, pi_x, response_time).
"""

import csv
import os
import sys
import time
from pathlib import Path

import requests

CHUNK_RANGES = {
    "master_file_1_0.txt": (1, 100000000000000000000000000),
    "master_file_2_0.txt": (1, 45216000000000),
    "master_file_2_1.txt": (45216000000000, 100000000000000000000000000),
    "master_file_4_0.txt": (1, 383026000000),
    "master_file_4_1.txt": (383027000000, 45216000000000),
    "master_file_4_2.txt": (45216100000000, 9412090000000000),
    "master_file_4_3.txt": (9412100000000000, 100000000000000000000000000),
    "master_file_8_0.txt": (1, 34845900000),
    "master_file_8_1.txt": (34846000000, 383026000000),
    "master_file_8_2.txt": (383027000000, 4175930000000),
    "master_file_8_3.txt": (4175940000000, 45216000000000),
    "master_file_8_4.txt": (45216100000000, 906642000000000),
    "master_file_8_5.txt": (906643000000000, 9412090000000000),
    "master_file_8_6.txt": (9412100000000000, 97577600000000000),
    "master_file_8_7.txt": (97577700000000000, 100000000000000000000000000),
    "master_file_16_0.txt": (1, 4052720000),
    "master_file_16_1.txt": (4052730000, 34845900000),
    "master_file_16_2.txt": (34846000000, 81574300000),
    "master_file_16_3.txt": (81574400000, 383026000000),
    "master_file_16_4.txt": (383027000000, 850310000000),
    "master_file_16_5.txt": (850311000000, 4175930000000),
    "master_file_16_6.txt": (4175940000000, 8848770000000),
    "master_file_16_7.txt": (8848780000000, 45216000000000),
    "master_file_16_8.txt": (45216100000000, 439358000000000),
    "master_file_16_9.txt": (439359000000000, 906642000000000),
    "master_file_16_10.txt": (906643000000000, 4739250000000000),
    "master_file_16_11.txt": (4739260000000000, 9412090000000000),
    "master_file_16_12.txt": (9412100000000000, 50849200000000000),
    "master_file_16_13.txt": (50849300000000000, 97577600000000000),
    "master_file_16_14.txt": (97577700000000000, 543059000000000000),
    "master_file_16_15.txt": (543060000000000000, 100000000000000000000000000),
    "master_file_32_0.txt": (1, 1716300000),
    "master_file_32_1.txt": (1716310000, 4052720000),
    "master_file_32_2.txt": (4052730000, 11481700000),
    "master_file_32_3.txt": (11481800000, 34845900000),
    "master_file_32_4.txt": (34846000000, 58210100000),
    "master_file_32_5.txt": (58210200000, 81574300000),
    "master_file_32_6.txt": (58210200000, 149384000000),
    "master_file_32_7.txt": (149385000000, 383026000000),
    "master_file_32_8.txt": (383027000000, 616668000000),
    "master_file_32_9.txt": (616669000000, 850310000000),
    "master_file_32_10.txt": (850311000000, 1839510000000),
    "master_file_32_11.txt": (1839520000000, 4175930000000),
    "master_file_32_12.txt": (4175940000000, 6512350000000),
    "master_file_32_13.txt": (6512360000000, 8848770000000),
    "master_file_32_14.txt": (8848780000000, 21851800000000),
    "master_file_32_15.txt": (21851900000000, 45216000000000),
    "master_file_32_16.txt": (45216100000000, 205716000000000),
    "master_file_32_17.txt": (205717000000000, 439358000000000),
    "master_file_32_18.txt": (439359000000000, 673000000000000),
    "master_file_32_19.txt": (673001000000000, 906642000000000),
    "master_file_32_20.txt": (906643000000000, 2402830000000000),
    "master_file_32_21.txt": (2402840000000000, 4739250000000000),
    "master_file_32_22.txt": (4739260000000000, 7075670000000000),
    "master_file_32_23.txt": (7075680000000000, 9412090000000000),
    "master_file_32_24.txt": (9412100000000000, 27485000000000000),
    "master_file_32_25.txt": (27485100000000000, 50849200000000000),
    "master_file_32_26.txt": (50849300000000000, 74213400000000000),
    "master_file_32_27.txt": (74213500000000000, 97577600000000000),
    "master_file_32_28.txt": (97577700000000000, 309417000000000000),
    "master_file_32_29.txt": (309418000000000000, 543059000000000000),
    "master_file_32_30.txt": (543060000000000000, 776701000000000000),
    "master_file_32_31.txt": (776702000000000000, 100000000000000000000000000),
}

x = 100

n_chunks = int(os.environ.get("NUM_CHUNKS") or 1)
print(f"n_chunks = {n_chunks}")

response_data: list[tuple[str | int, str | int, str | int, str | float]] = [
    ("n_chunks", "x", "pi_x", "response_time")
]


def make_request(x: int, n_chunks: int):
    for chunk in range(n_chunks):
        file_name = f"master_file_{n_chunks}_{chunk}.txt"
        os.path.join("data", file_name)
        chunk_range = CHUNK_RANGES[file_name]
        if chunk_range[0] <= x <= chunk_range[1]:
            try:
                start_time = time.time()
                response = requests.get(
                    f"http://searcher{chunk}:80/pi_fn/{x}?num_chunks={n_chunks}&chunk_index={chunk}"
                )
                end_time = time.time()

            except requests.exceptions.RequestException:
                sys.exit(1)

            if response.status_code != 200:
                print("error 2")
                sys.exit(2)

            response_time = end_time - start_time
            try:
                response_json = response.json()

                assert isinstance(response_json["x"], int) and isinstance(
                    response_json["pi_x"], int
                )

                response_data.append(
                    (n_chunks, response_json["x"], response_json["pi_x"], response_time)
                )

            except AssertionError as ae:
                raise TypeError from ae
            except TypeError:
                response_data.append((n_chunks, x, -1, response_time))
                sys.exit(3)


if __name__ == "__main__":
    print("Waiting for searchers to start...")
    time.sleep(5)
    print("Searchers started\n")
    with open(os.path.join("data", "random_integers.txt"), encoding="UTF-8") as f:
        for x in f:
            make_request(int(x), n_chunks)

    Path("results/response_data").mkdir(parents=True, exist_ok=True)

    with open(
        os.path.join("results", "response_data", f"response_data_{n_chunks}.csv"),
        "w+",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.writer(f)
        writer.writerows(response_data)

    print("response_data.csv written")
