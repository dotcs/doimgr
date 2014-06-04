import os
import sys
import json
import urllib.parse
import httplib2
import logging
import re

from lib.search.result import SearchResult
from lib.doi import DOI
from lib.fulltexturl import FullTextURL

class Request(object):
    """
    Manages requests to the background online service at `crossref.org` using
    the official API.

    """
    URL_PROTOCOL = "http"
    URL_SERVICE_DOIS = "api.crossref.org/works"

    def __init__(self):
        pass

    def prepare_search_query(self, string, sort='score', order='desc', \
            year=None, type=None, rows=20):
        valid_sort_methods = ('score', 'updated', 'deposited', 'indexed',
                'published')
        if sort not in valid_sort_methods:
            raise ValueError("Sort method not supported. Valid values are: \
{}".format(", ".join(valid_sort_methods)))

        valid_order_methods = ('asc', 'desc')
        if order not in valid_order_methods:
            raise ValueError("Order method not supported. Valid values are: \
{}".format(", ".join(valid_order_methods)))

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

    def prepare_citation_query(self, doi_identifier):
        doi = DOI(doi_identifier)
        return doi.get_identifier() + '/transform'

    def search(self, query):
        url = "{}://{}?{}".format(self.URL_PROTOCOL, \
                self.URL_SERVICE_DOIS, query)
        logging.debug("Search URL: {}".format(url))
        response = self._request(url)
        return response

    def print_search_content(self, content, show_authors=False,
            show_type=False, show_publisher=False, show_url=False):
        base_template = "{score:.2f} - {year:4d} - {doi:40} - {title}"
        template = base_template

        if show_authors:
            template += "\n  AUTHORS   : {authors}"
        if show_type:
            template += "\n  TYPE      : {type}"
        if show_publisher:
            template += "\n  PUBLISHER : {publisher}"
        if show_url:
            template += "\n  URL       : {url}"

        for result in content.get('items', ()):
            sr = SearchResult(result)
            payload = {
                "score"     : sr.get_score(),
                "year"      : sr.get_year(),
                "doi"       : sr.get_doi().get_identifier(),
                "title"     : sr.get_title(),
                "authors"   : sr.get_authors(),
                "type"      : sr.get_type(),
                "publisher" : sr.get_publisher(),
                "url"       : sr.get_url()
            }

            print(template.format(**payload))

    def citation(self, query, style='bibtex'):
        url = "{}://{}/{}".format(self.URL_PROTOCOL, self.URL_SERVICE_DOIS,
                query)
        headers={'Accept':'text/x-bibliography; style={}'.format(style)}

        logging.debug("Cite URL: {}".format(url))
        logging.debug("Query headers: {}".format(headers))
        logging.debug("Style: {}".format(style))

        response = self._request(url, headers, json_message=False)

        return response.strip()

    def print_citation(self, content):
        print(self.__clean_html(content))

    def get_download_links(self, identifier):
        url = "{}://{}/{}".format(self.URL_PROTOCOL, self.URL_SERVICE_DOIS,
                identifier)
        logging.debug("Query URL: {}".format(url))

        response = self._request(url)

        links = []
        for link in response.get('link', ()):
            content_version = link['content-version']
            license = self._find_license(response, content_version)
            links.append(FullTextURL(link.get("URL", ""), license.get("URL",
                None)))

        return links

    def _find_license(self, response, content_version):
        for license in response.get('license', ()):
            if license.get("content-version", "") == content_version:
                return license
        return None

    def _request(self, url, 
            headers={'content-type': 'application/json'}, method="GET",
            json_message=True):

        h = httplib2.Http(".cache")
        resp, content = h.request(url, method, headers=headers)

        request_status = int(resp['status'])
        if request_status != 200:
            raise RuntimeError("The server responded with code {:d}, which the \
script cannot deal with. Aborting.".format(request_status))

        if json_message:
            return json.loads(content.decode('utf-8'))['message']
        return content.decode('utf-8')

    def __clean_html(self, raw_html):
        regex = re.compile(r'<(.*?)>(.*?)</\1>')
        return re.sub(regex, r"\2", raw_html)
