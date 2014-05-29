#!/usr/bin/env python

import os
import sys
import argparse
import logging

from lib.search.request import Request

logging.basicConfig(level=logging.DEBUG)

def main(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Command line based tool to request DOI data and convert \
it to BibTex entries.')
    subparsers = parser.add_subparsers()

    parser_search = subparsers.add_parser('search', help='Search database for \
a published article to find the relevant DOI')
    parser_search.add_argument('query', type=str, help='search string')
    parser_search.add_argument('--sort', type=str, default='score', choices=['score', \
        'year'], help='sorting of search queries')

    parser_doi = subparsers.add_parser('doi', help='Use DOI to request \
specific data format like BibTex')
    parser_doi.add_argument('identifier', type=str, help='DOI identifier')
    parser_doi.add_argument('-f', '--format', type=str, default='bibtex', \
            choices=['bibtex', 'ris', 'apa', 'harvard', 'ieee', 'mla', \
            'vancouver', 'chicago'], help='output format when searching for a \
specific DOI')

    args = parser.parse_args()

    if hasattr(args, 'query'):
        logging.debug('Arguments match to perform search')
        req = Request()
        results = req.search(req.prepare_search_query(args.query, args.sort))
        req.print_search_content(results)

    if hasattr(args, 'identifier'):
        logging.debug('Arguments match to request single DOI')
        req = Request()
        result = req.citation(req.prepare_citation_query(args.identifier, args.format))
        req.print_citation(result)

if __name__ == "__main__":
    main(sys.argv)
