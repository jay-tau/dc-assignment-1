"""
Used to create docker-compose file for searcher workers based on the number of workers.

Creates a docker-compose file `docker-compose-{n}.yaml` where n is the number of workers.
The docker-compose file will contain n+1 services:
  1. load-balancer
  2. searcher0
  3. searcher1
  ...
  n. searcher{n-1}
The load-balancer service will have an environment variable NUM_CHUNKS set to n.
The searcher services will have their ports exposed from 8000 to 8000+n-1.
The searcher services will have a volume mounted to the data directory.
"""

import os
import sys

n = int(input("Number of searcher workers: ").strip() or 1)  # Default value is 1

with open(
    os.path.join("docker-compose", f"docker-compose-{n}.yaml"), "w", encoding="utf-8"
) as f:
    sys.stdout = f  # Redirect stdout to file
    print("services:")
    print(
        f"""  load-balancer:
    image: load-balancer
    volumes:
      - ../data:/code/data
    environment:
      - NUM_CHUNKS={n}
    depends_on:"""
    )
    for i in range(n):
        print(f"      - searcher{i}")
    for i in range(n):
        print(
            f"""  searcher{i}:
    image: searcher-worker
    ports:
      - {8000+i}:80
    volumes:
      - ../data:/code/data"""
        )
