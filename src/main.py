from islandora import ContentModel as CM
from islandora_scraper import IslandoraScraper
import newspapers
from import_helper import ImportHelper
import utils
import argparse


def main():
    base_parser = argparse.ArgumentParser()
    base_parser.add_argument('-o', '--output_dir', help='The directory to save files in')
    sub_parsers = base_parser.add_subparsers(required=True, dest='command')

    dl_parser = sub_parsers.add_parser('download')
    dl_parser.add_argument('url', help='The url of the islandora instance ex: "https://islandnewspapers.ca/islandora"')
    dl_parser.add_argument('-c', '--count', type=int, default=20, help='The number of results to pull from')
    dl_parser.add_argument('-q', '--query', default='', help='The term to search for when downloading issues')
    dl_parser.add_argument('-l', '--light_weight', action='store_true', help='Download pages without OBJ')

    pr_parser = sub_parsers.add_parser('prep')
    pr_parser.add_argument('-f', '--format', choices=['dir', 'zip'], default='dir',
                           help='The format to save the issues in.')
    pr_parser.add_argument('-i', '--input', default='data/download')

    args = base_parser.parse_args()

    output = args.output_dir
    if args.command == 'download':
        page_cm = newspapers.page_light_cm if args.light_weight else newspapers.page_cm
        if output is None:
            output = 'data/download'
        utils.download(query=args.query, num=args.count, directory=output, url=args.url, page_cm=page_cm)
    elif args.command == 'prep':
        if output is None:
            output = 'data/ingest'
        ih = ImportHelper(ingest_dir=output, download_dir=args.input)
        ih.load_dir()
        ih.prep_papers()
        ih.prep_issues(method=args.format)
    else:
        print('Invalid command')


if __name__ == '__main__':
    main()
