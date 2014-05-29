#!/usr/bin/env python
import os
import sys
import argparse
import logging

from lib.search.request import Request

def main(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Command line based tool to request DOI data and convert \
it to BibTex entries.')
    subparsers = parser.add_subparsers()

    parser_search = subparsers.add_parser('search', help='Search database for \
a published article to find the relevant DOI')
    parser_search.add_argument('query', type=str, help='search string')
    parser_search.add_argument('--show-authors', action='store_true', help='if \
            set additional author information is shown')
    parser_search.add_argument('--sort', type=str, default='score', \
            choices=['score', 'updated', 'deposited', 'indexed', 'published'], \
            help='sorting of search queries')
    parser_search.add_argument('--order', type=str, default='desc', \
            choices=['asc', 'desc'], help='ordering of search queries')
    parser_search.add_argument('--year', type=int, help='limit the year')
    parser_search.add_argument('--rows', type=int, default=20, help='number of \
rows to load')
    # receive allowed types via http://api.crossref.org/types
    parser_search.add_argument('--type', type=str, choices=[
        'book',
        'book-chapter',
        'book-entry',
        'book-part',
        'book-section',
        'book-series',
        'book-set',
        'book-track',
        'component',
        'dataset',
        'dissertation',
        'edited-book',
        'journal',
        'journal-article',
        'journal-issue',
        'journal-volume',
        'monograph',
        'other',
        'proceedings',
        'proceedings-article',
        'reference-book',
        'report',
        'standard',
        'standard-series',
        ], help='limit the type')

    parser_doi = subparsers.add_parser('cite', help='Cite article based on \
DOI in different citation formats')
    parser_doi.add_argument('identifier', type=str, help='DOI identifier')
    parser_doi.add_argument('-f', '--format', type=str, default='bibtex', \
            choices=['bibtex', 'ris', 'apa', 'harvard', 'ieee', 'mla', \
            'vancouver', 'chicago'], help='output format when searching for a \
specific DOI')

    parser.add_argument('-q', '--quiet', action='store_true', help='turns off \
all unnecessary outputs; use this for scripting')
    parser.add_argument('--log-level', type=str, choices=['info', 'debug'], \
            default='info', help='set the logging level')

    args = parser.parse_args()

    # set the logging levels according to the users choice
    if args.quiet:
        level = logging.CRITICAL
    else:
        level = logging.INFO
        if args.log_level == 'debug':
            level = logging.DEBUG
    logging.basicConfig(level=level)

    if hasattr(args, 'query'):
        logging.debug('Arguments match to perform search')
        req = Request()
        results = req.search(req.prepare_search_query(args.query, args.sort, \
            args.order, args.year, args.type, args.rows))
        req.print_search_content(results, args.show_authors)

    if hasattr(args, 'identifier'):
        logging.debug('Arguments match to request single DOI')
        req = Request()
        result = req.citation(req.prepare_citation_query(args.identifier, args.format))
        req.print_citation(result)

if __name__ == "__main__":
    main(sys.argv)
