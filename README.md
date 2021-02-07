# Islandora Scraping Utils

This is a package for scraping data off of an existing instace of Islandora, and preparing it to ingest into another.

## Getting Started

Setup:

```
pip install -r requirements.txt
```

## Usage

```
usage: main.py [-h] [-d DEST] {download,prep} ...

positional arguments:
  {download,prep}

optional arguments:
  -h, --help            show this help message and exit
  -d DEST, --dest DEST  The directory to save files in
```

```
usage: main.py download [-h] [-c COUNT] [-q QUERY] [-l] url

positional arguments:
  url                   The url of the islandora instance ex: "https://islandnewspapers.ca/islandora"

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        The number of results to pull from
  -q QUERY, --query QUERY
                        The term to search for when downloading issues
  -l, --light_weight    Download pages without OBJ
```

```
usage: main.py prep [-h] [-i {dir,zip}] [-n {zip,marcxml}] [-s SOURCE]

optional arguments:
  -h, --help            show this help message and exit
  -i {dir,zip}, --issues {dir,zip}
                        The format to save the issues in.
  -n {zip,marcxml}, --newspapers {zip,marcxml}
                        The format to save the newspapers in.
  -s SOURCE, --source SOURCE
```