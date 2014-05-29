import os
import sys
import json
import urllib.parse
import httplib2
import logging

from lib.search.result import SearchResult
from lib.doi import DOI

class Request(object):
    """
    Manages requests to the background online service at `crossref.org` using
    the official API.

    """
    URL_PROTOCOL = "http"
    URL_SERVICE_DOIS = "search.crossref.org/dois"
    URL_SERVICE_CITATION = "search.crossref.org/citation"

    def __init__(self):
        pass

    def prepare_search_query(self, string, sort, year, type):
        payload = {'q': string, 'sort': sort}
        if year is not None:
            payload['year'] = year
        if type is not None:
            payload['type'] = type
        return urllib.parse.urlencode(payload)

    def prepare_citation_query(self, doi_identifier, cite_format):
        doi = DOI(doi_identifier)
        payload = {'format': cite_format, 'doi': doi.get_identifier()}
        return urllib.parse.urlencode(payload)

    def search(self, query):
        url = "{}://{}?{}".format(self.URL_PROTOCOL, \
                self.URL_SERVICE_DOIS, query)
        logging.debug("Search URL: {}".format(url))

        h = httplib2.Http(".cache")
        resp, content = h.request(url, "GET", headers = \
                { 'content-type': 'application/json' })

        request_status = int(resp['status'])
        if request_status != 200:
            raise RuntimeError("The server responded with code {:d}, which the \
script cannot deal with. Aborting.".format(status))

        return content.decode('utf-8')

    def print_search_content(self, content):
        json_content = json.loads(content)
        for result in json_content:
            sr = SearchResult(result)
            print("{:3d} - {:4d} - {:40} - {}". \
                    format(sr.get_normalized_score(), sr.get_year(), \
                    sr.get_doi().get_identifier(), sr.get_title()))

    def citation(self, query):
        url = "{}://{}?{}".format(self.URL_PROTOCOL, self.URL_SERVICE_CITATION, query)
        logging.debug("Cite URL: {}".format(url))

        h = httplib2.Http(".cache")
        resp, content = h.request(url, "GET")

        request_status = int(resp['status'])
        if request_status != 200:
            raise RuntimeError("The server responded with code {:d}, which the \
script cannot deal with. Aborting.".format(status))

        return content.decode('utf-8')

    def print_citation(self, content):
        print(content)
