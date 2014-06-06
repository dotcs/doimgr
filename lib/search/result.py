import os
import sys
import re
from datetime import datetime

from lib.doi import DOI

class SearchResult(object):
    """
    Representation of an individual search result.

    """
    UNKNOWN_TITLE = "Unknown title"
    UNKNOWN_YEAR = 0
    UNKNOWN_AUTHORS = ''

    def __init__(self, json=None):
        self.authors   = None
        self.doi       = None
        self.publisher = None
        self.score     = None
        self.subtitle  = None
        self.title     = None
        self.type      = None
        self.year      = None
        self.url       = None

        if json is not None:
            self.parse_json(json)

    def parse_json(self, json):
        self.doi = DOI(json.get('URL', None))
        self.score = float(json.get('score', 0.))
        try:
            self.title = self.format_title(json['title'][0])
        except (IndexError, KeyError):
            self.title = self.UNKNOWN_TITLE

        #self.timestamp = float(json['deposited']['timestamp'])/1000.
        try:
            self.year = int(json['issued']['date-parts'][0][0])
        except (TypeError, KeyError, IndexError):
            self.year = self.UNKNOWN_YEAR
        try:
            self.authors = self.__format_authors(json['author'])
        except KeyError:
            self.authors = self.UNKNOWN_AUTHORS
        self.type = json.get('type', None)
        self.publisher = json.get('publisher', None)
        self.url = json.get('URL', None)

    def format_title(self, title):
        def repl_func(m):
            """
            Process regular expression match groups for word upper-casing problem
            Credits: http://stackoverflow.com/a/1549983/434227
            """
            return m.group(1) + m.group(2).upper()

        if title.isupper():
            # We are unable to reconstruct capitalized words, when everything
            # char is capitalized.
            # The best we can do in this case is to lower everything and let
            # our method do the rest.
            # Using this method will lose capitalized word though.
            title = title.lower()

        title = self.__clean_html(title).strip()
        return re.sub("(^|\s)(\S)", repl_func, title)

    def get_doi(self):
        return self.doi

    def get_score(self):
        return self.score

    def get_title(self):
        return self.title

    def get_year(self):
        #return datetime.fromtimestamp(self.timestamp).year
        return self.year

    def get_authors(self):
        return self.authors

    def get_type(self):
        return self.type

    def get_publisher(self):
        return self.publisher

    def get_url(self):
        return self.url

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.doi.get_identifier()

    def __clean_html(self, raw_html):
        regex = re.compile(r'<(.*?)>(.*?)</\1>')
        return re.sub(regex, r"\2", raw_html)

    def __format_authors(self, author_list, limit=3):
        author_temp = []
        for i, author in enumerate(author_list):
            if i >= limit: break
            author_temp.append(", ".join(author[i] for i in ('family', 'given')))
        output = "; ".join(author_temp)
        if len(author_list) > limit:
            output += " et al."
        return output
