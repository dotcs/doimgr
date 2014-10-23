#!/usr/bin/env python
# -----------------------------------------------------------------------------
# (c) 2014 by Fabian Mueller <software@crashsource.de>
# 
# THIS SOFTWARE IS RELEASED UNDER THE MIT LICENSE.
# FOR MORE INFORMATION SEE THE LINCENSE FILE.
# -----------------------------------------------------------------------------
import os
import sys
import argparse
import logging
import configparser

from lib.search.request import Request
from lib.downloader import Downloader
from lib.api import API
from lib.clipboard import Clipboard
from lib.bulkconverter import BulkConverter

# MAIN VERSION OF THIS PROGRAM
__version_info__ = (0, 1, 2)
__version__      = '.'.join(map(str, __version_info__))

api = API()

def main(argv):
    config = configparser.ConfigParser()
    config_path = os.path.expanduser(os.path.join("~", ".doimgrrc"))
    if os.path.isfile(config_path):
        config.read(config_path)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Command line based tool to request DOI data and convert \
it to BibTex entries.')
    subparsers = parser.add_subparsers()

    parser_search = subparsers.add_parser('search', 
        help='Search database for published articles to find relevant DOIs',
        description="""Searches database for published articles. This can be
used to find a specific DOI or getting information about a keyword/topic.""")
    parser_search.add_argument('query', type=str, help='search string')
    parser_search.add_argument('--show-authors', action='store_true',
        default=config.getboolean('search', 'show-authors', fallback=False),
        help='if set additional author information is shown')
    parser_search.add_argument('--show-type', action='store_true',
        default=config.getboolean('search', 'show-type', fallback=False),
        help='if set additional information about the type is shown')
    parser_search.add_argument('--show-publisher', action='store_true',
        default=config.getboolean('search', 'show-publisher', fallback=False),
        help='if set additional information about the publisher is shown')
    parser_search.add_argument('--show-url', action='store_true',
        default=config.getboolean('search', 'show-url', fallback=False),
        help='if set a URL to the document is shown')
    allowed_sort_types=['score', 'updated', 'deposited', 'indexed', 'published']
    parser_search.add_argument('--sort', type=str, choices=allowed_sort_types,
        default=config.get('search', 'sort', fallback='score'),
        help='sorting of search queries; allowed values are {}'\
            .format(", ".join(allowed_sort_types)), metavar='')
    parser_search.add_argument('--order', type=str,
        choices=['asc', 'desc'],
        default=config.get('search', 'order', fallback='desc'),
        help='ordering of search queries')
    parser_search.add_argument('--year', type=int,
        default=config.getint('search', 'year', fallback=None),
        help='limit the year')
    parser_search.add_argument('--rows', type=int,
        default=config.getint('search', 'rows', fallback=20),
        help='number of rows to load')
    parser_search.add_argument('--color', action="store_true",
        default=config.getboolean('search', 'color', fallback=False),
        help='if set, colored output is used')
    valid_colors = ['black', 'cyan', 'magenta', 'yellow', 'blue', 'green',
            'red', 'white']
    parser_search.add_argument('--color-doi', type=str,
        default=config.get('search', 'color-doi', fallback='red'),
        choices=valid_colors, help='color for DOIs')
    parser_search.add_argument('--color-title', type=str,
        default=config.get('search', 'color-title', fallback='green'),
        choices=valid_colors, help='color for titles')
    parser_search.add_argument('--color-more', type=str,
        default=config.get('search', 'color-more', fallback='blue'),
        choices=valid_colors, help='color for additional information such as \
authors, URLs, etc.')

    # receive allowed types via http://api.crossref.org/types
    allowed_types = api.get_valid_types()
    parser_search.add_argument('--type', type=str, choices=allowed_types,
        default=config.get('search', 'type', fallback=None),
        help='selects a single type; allowed values are {}'.format(", "\
            .join(allowed_types)),
        metavar='')
    parser_search.set_defaults(which_parser='search')

    parser_cite = subparsers.add_parser('cite',
        help='Cite article based on DOI in different citation formats', 
        description="""Cite articles with a known DOI. Formatting can be done
using the `style`-parameter and supports hundreds of different citation
formats. A full list of supported formats can be found in the subfolder
`API/styles.txt`. The most common ones are `apa` and `bibtex`.""")
    parser_cite.add_argument('identifier', type=str, help='DOI identifier')
    parser_cite.add_argument('-s', '--style', type=str,
        default=config.get('cite', 'style', fallback="bibtex"),
        help='Citation style')
    parser_cite.add_argument('-c', '--copy', action='store_true',
        default=config.get('cite', 'copy', fallback=False),
        help="""Copies the result to the system clipboard""")
    parser_cite.set_defaults(which_parser='cite')

    parser_download = subparsers.add_parser('download',
        help='Download articles based on their DOI', 
        description="""Downloads articles, if a full text verison is provided
by the authors.""")
    parser_download.add_argument('identifier', type=str, help='DOI identifier')
    parser_download.add_argument('-d', '--destination', type=str,
        default=config.get('download', 'destination', fallback="."),
        help='download destination')
    parser_download.set_defaults(which_parser='download')

    parser_bulk = subparsers.add_parser('bulk',
        help='Mass converting for multiple DOIs listed in a single file.',
        description="""Mass converting for multiple DOIs listed in a single file.""")
    parser_bulk.add_argument('input', type=argparse.FileType('r'), 
        help='input file path', nargs='?', default=sys.stdin)
    parser_bulk.add_argument('output', type=argparse.FileType('w'),
        help='output file path', nargs='?', default=sys.stdout)
    parser_bulk.add_argument('-s', '--style', type=str,
        default=config.get('bulk', 'style', fallback="bibtex"),
        help='Citation style')
    parser_bulk.set_defaults(which_parser='bulk')

    parser_service = subparsers.add_parser('service',
        help='Provices service functions for the API such as rebuilding the \
database of valid types and styles', 
        description="""Provices service functions for the API such as
rebuilding the database of valid types and styles""")
    parser_service.add_argument('--rebuild-api-types', action='store_true',
            help='Rebuild the types, that are accepted on API requests')
    parser_service.add_argument('--rebuild-api-styles', action='store_true',
            help='Rebuild the styles, that are accepted on API requests')
    parser_service.set_defaults(which_parser='service')

    parser.add_argument('-q', '--quiet', action='store_true', 
        default=config.getboolean('general', 'quiet', fallback=False),
        help='turns off all unnecessary outputs; use this for scripting')
    parser.add_argument('--log-level', type=str, choices=['info', 'debug'],
        default=config.get('general', 'log-level', fallback="info"),
        help='set the logging level')
    parser.add_argument('--version', action="store_true",
        help='shows the version of doimgr')

    args = parser.parse_args()

    if args.version:
        print("doimgr version: {}".format(__version__))
        sys.exit()

    # set the logging levels according to the users choice
    if args.quiet:
        level = logging.CRITICAL
    else:
        level = logging.INFO
        if args.log_level == 'debug':
            level = logging.DEBUG
    logging.basicConfig(level=level)

    logging.debug("doimgr version {}".format(__version__))

    if hasattr(args, 'which_parser'):
        if args.which_parser == 'search':
            logging.debug('Arguments match to perform search')
            req = Request()
            if sys.stdout.isatty():
                # only allow colors when the script's output is not redirected
                req.set_colored_output(args.color, doi=args.color_doi,
                        title=args.color_title, more=args.color_more)
            else:
                logging.debug('Colors have been disabled due to detected \
reconnect')
            results = req.search(req.prepare_search_query(args.query,
                args.sort, args.order, args.year, args.type, args.rows))
            req.print_search_content(results, args.show_authors,
                    args.show_type, args.show_publisher, args.show_url)

        elif args.which_parser == 'cite':
            logging.debug('Arguments match to request single DOI')

            # check if given style is valid
            # this is not done via argparse directly due to the amount of
            # possible parameters
            styles = api.get_valid_styles()
            if args.style not in styles:
                raise ValueError("Given style \"{}\" is not valid. \
    Aborting.".format(args.style))

            req = Request()
            result = req.citation(req.prepare_citation_query(args.identifier),
                    style=args.style)
            req.print_citation(result)
            if args.copy:
                Clipboard.copy_to(result)

        elif args.which_parser == 'download':
            logging.debug('Arguments match to download single DOI')

            try:
                os.makedirs(os.path.expanduser(args.destination))
                logging.debug("Destination dir {} created.".format(
                    args.destination))
            except FileExistsError:
                logging.debug("Destination dir {} does already exists".format(
                    args.destination))

            req = Request()
            links = req.get_download_links(args.identifier)
            for link in links:
                url = link.get_url()
                d = Downloader()
                filepath = d.download(url, 
                    os.path.expanduser(args.destination),
                    "{}.pdf".format(args.identifier.replace("/", "_")))
                if filepath is not None:
                    logging.info("Saved file as {}".format(filepath))

            if len(links) == 0:
                logging.info("No valid download URLs found. Aborting.")

        elif args.which_parser == 'bulk':
            logging.debug('Arguments match with bulk conversion')

            # check if given style valid
            # this is not done via argparse directly due to the amount of
            # possible parameters
            styles = api.get_valid_styles()
            if args.style not in styles:
                raise ValueError("Given style \"{}\" is not valid. \
    Aborting.".format(args.style))

            b = BulkConverter()
            if args.output == sys.stdout:
                # switch to quiet mode, since we do not want to place
                # unneccesary messages on stdout
                logging.getLogger().setLevel(logging.CRITICAL)
            b.run(args.input, args.output, style=args.style)

        elif args.which_parser == 'service':
            logging.debug('Arguments match with service call')

            if args.rebuild_api_types:
                api.rebuild_valid_identifier(api.TYPE_TYPES)

            if args.rebuild_api_styles:
                api.rebuild_valid_identifier(api.TYPE_STYLES)

if __name__ == "__main__":
    main(sys.argv)
