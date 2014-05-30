import os
import sys
import json
import urllib.parse
import httplib2
import logging
import re

from lib.search.result import SearchResult
from lib.doi import DOI

class Request(object):
    """
    Manages requests to the background online service at `crossref.org` using
    the official API.

    """
    URL_PROTOCOL = "http"
    URL_SERVICE_DOIS = "api.crossref.org/works"

    def __init__(self):
        pass

    def prepare_search_query(self, string, sort, order, year, type, rows):
        filters = []
        payload = {'query': string, 'sort': sort, 'order': order, 'rows': rows}
        if year is not None:
            filters.append(('from-pub-date', year))
        if type is not None:
            filters.append(('type', type))

        # load all filter values
        payload['filter'] = ','.join(['{}:{}'.format(key, value) for key, value\
            in filters])

        return urllib.parse.urlencode(payload)

    def prepare_citation_query(self, doi_identifier, cite_format):
        doi = DOI(doi_identifier)
        return "{doi}/transform/{format}".format(**{
            'doi'    : doi.get_identifier(),
            'format' : \
            self.__get_format_content_type_by_identifier(cite_format),
        })

    def __get_format_content_type_by_identifier(self, identifier):
        if identifier == 'bibtex':
            return 'application/x-bibtex'
        if identifier == 'citeproc-json':
            return 'application/vnd.citationstyles.csl+json'
        if identifier == 'datacite-xml':
            return 'application/vnd.datacite.datacite+xml'
        if identifier == 'rdf-turtle':
            return 'text/turtle'
        if identifier == 'rdf-xml':
            return 'application/rdf+xml'
        if identifier == 'ris':
            return 'application/x-research-info-systems'
        if identifier == 'text':
            return 'text/x-bibliography'
        if identifier == 'unixref-xml':
            return 'application/vnd.crossref.unixref+xml'
        raise ValueError("Identifier {} not known. Aborting.".format(identifier))

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
script cannot deal with. Aborting.".format(request_status))

        return content.decode('utf-8')

    def print_search_content(self, content, show_authors, show_type):
        base_template = "{score:.2f} - {year:4d} - {doi:40} - {title}"
        template = base_template

        if show_authors:
            template += "\n  AUTHORS: {authors}"
        if show_type:
            template += "\n  TYPE: {type}"

        json_content = json.loads(content)
        for result in json_content['message']['items']:
            sr = SearchResult(result)
            payload = {
                    "score"   : sr.get_score(),
                    "year"    : sr.get_year(),
                    "doi"     : sr.get_doi().get_identifier(),
                    "title"   : sr.get_title(),
                    "authors" : sr.get_authors(),
                    "type"    : sr.get_type(),
            }

            print(template.format(**payload))

    def citation(self, query):
        url = "{}://{}/{}".format(self.URL_PROTOCOL, self.URL_SERVICE_DOIS, query)
        logging.debug("Cite URL: {}".format(url))

        h = httplib2.Http(".cache")
        resp, content = h.request(url, "GET")

        request_status = int(resp['status'])
        if request_status != 200:
            raise RuntimeError("The server responded with code {:d}, which the \
script cannot deal with. Aborting.".format(request_status))

        return content.decode('utf-8')

    def print_citation(self, content):
        print(self.__clean_html(content))

    def __clean_html(self, raw_html):
        regex = re.compile(r'<(.*?)>(.*?)</\1>')
        return re.sub(regex, r"\2", raw_html)
