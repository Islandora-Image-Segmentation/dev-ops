from islandora import ContentModel as CM
from islandora_scraper import IslandoraScraper
import newspapers
from import_helper import ImportHelper
import utils
import argparse


def main():
    base_parser = argparse.ArgumentParser()
    base_parser.add_argument('-d', '--dest', help='The directory to save files in')
    sub_parsers = base_parser.add_subparsers(required=True, dest='command')

    dl_parser = sub_parsers.add_parser('download')
    dl_parser.add_argument('url', help='The url of the islandora instance ex: "https://islandnewspapers.ca/islandora"')
    dl_parser.add_argument('-c', '--count', type=int, default=20, help='The number of results to pull from')
    dl_parser.add_argument('-q', '--query', default='', help='The term to search for when downloading issues')
    dl_parser.add_argument('-l', '--light_weight', action='store_true', help='Download pages without OBJ')

    pr_parser = sub_parsers.add_parser('prep')
    pr_parser.add_argument('-i', '--issues', choices=['dir', 'zip'], default='dir',
                           help='The format to save the issues in.')
    pr_parser.add_argument('-n', '--newspapers', choices=['dir', 'zip', 'marcxml'], default='dir',
                           help='The format to save the newspapers in.')
    pr_parser.add_argument('-s', '--source', default='data/download')

    args = base_parser.parse_args()

    dest = args.dest
    if args.command == 'download':
        page_cm = newspapers.page_light_cm if args.light_weight else newspapers.page_cm
        if dest is None:
            dest = 'data/download'
        utils.download(query=args.query, num=args.count, directory=dest, url=args.url, page_cm=page_cm)
    elif args.command == 'prep':
        if dest is None:
            dest = 'data/ingest'
        ih = ImportHelper(ingest_dir=dest, download_dir=args.source)
        ih.load_dir()
        if args.newspapers == 'dir':
            ih.prep_papers_dir()
        elif args.newspapers == 'zip':
            ih.prep_papers_zip()
        elif args.newspapers == 'marcxml':
            ih.prep_papers_marc()
        ih.prep_issues(method=args.issues)
    else:
        print('Invalid command')


if __name__ == '__main__':
    main()
