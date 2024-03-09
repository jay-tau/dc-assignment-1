"""
This module contains the search operation.

The search operation is responsible for searching for a value in the master file.

The master file is split into multiple chunks, and each chunk is stored in a separate file.

The search operation reads the chunk file and searches for the value in the chunk.

If the value is found, the search operation returns the value.

If the value is not found, the search operation returns -1.

The search operation is implemented using a FastAPI application.

The search operation is exposed as an HTTP GET endpoint.

The search operation accepts the following query parameters:
- x: The value to search for.
- num_chunks: The number of chunks in the master file. (Default: 1)
- chunk_index: The index of the chunk to search in. (Default: 0)

The search operation returns a JSON response with the following fields:
- x: The value that was searched for.
- pi_x: The value of pi at the searched value. (If the value was found)
- If the value was not found, the search operation returns -1.

The search operation is implemented using the following steps:
1. Validate the query parameters.
2. Read the chunk file.
3. Search for the value in the chunk file.
4. Return the result.
"""

import os
from datetime import datetime

from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/")
def read_root():
    """Return the current time."""
    return {"current_time": datetime.now()}


@app.get("/pi_fn/{x}")
def search(x: int, num_chunks: int = 1, chunk_index: int = 0):
    """Search for the value in the master file and return the result."""

    if num_chunks < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="num_chunks must be > 1"
        )
    if chunk_index < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="chunk_index must be >= 0"
        )
    if chunk_index >= num_chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="chunk_index must be < num_chunks",
        )

    file_name = f"master_file_{num_chunks}_{chunk_index}.txt"
    file_path = os.path.join("data", file_name)

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            split_line = line.split()

            try:
                assert len(split_line) == 3
            except AssertionError:
                continue

            try:
                x_val = int(split_line[0])
                pi_val = int(split_line[1])
            except ValueError:
                continue

            if x_val >= x:
                return {"x": x_val, "pi_x": pi_val}

    return -1
