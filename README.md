# Islandora Scraping Utils

This is a package for scraping data off of an existing instace of Islandora, and preparing it to ingest into another.

## Getting Started

Setup:

```
pip install -r requirements.txt
```

## Usage

```
usage: main.py [-h] [-o OUTPUT_DIR] {download,prep} ...

positional arguments:
  {download,prep}

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to save files in
```

```
usage: main.py download [-h] [-c COUNT] [-q QUERY] [-l LIGHT_WEIGHT] url

positional arguments:
  url                   The url of the islandora instance ex:
                        "https://islandnewspapers.ca/islandora"

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        The number of results to pull from
  -q QUERY, --query QUERY
                        The term to search for when downloading issues
  -l LIGHT_WEIGHT, --light_weight LIGHT_WEIGHT
                        Download pages without OBJ
```

```
usage: main.py prep [-h] [-f {dir,zip}] [-i INPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f {dir,zip}, --format {dir,zip}
                        The format to save the issues in.
  -i INPUT, --input INPUT
```