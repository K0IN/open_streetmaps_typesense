# Using typesense with german open street map data

This is a small example on how to use typesense with german open street map data.

## Data

The data is from the [geofabrik](https://download.geofabrik.de/europe/germany.html) website.
Which are open source and free to use german open street map data.

## Setup

1. Start the docker container with the following command:

```bash
docker compose up
```

2. Import the data into typesense (this might take a while):

```bash
./download-and-import.sh
```

3. Start the search cli:

```bash
python3 search.py
```

## Demo

[![asciicast](https://asciinema.org/a/bJMOlPe5F4mFLY0Rl6fiJSOp3.svg)](https://asciinema.org/a/kJBHBRpN09ZcPC4hUzjM5R9rL)
