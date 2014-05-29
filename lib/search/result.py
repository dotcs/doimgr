import os
import sys
import re

from lib.doi import DOI

class SearchResult(object):
    """
    Representation of an individual search result.

    """
    def __init__(self, json=None):
        self.coins = None
        self.doi = None
        self.full_citation = None
        self.normalized_score = None
        self.score = None
        self.title = None
        self.year = None

        if json is not None:
            self.parse_json(json)

    def parse_json(self, json):
        self.coins = json['coins']
        self.doi = DOI(json['doi'])
        self.full_citation = json['fullCitation']
        self.normalized_score = int(json['normalizedScore'])
        self.score = float(json['score'])
        self.title = self.__clean_html(json['title']).strip().title()
        # set year to 0 if unknown
        self.year = 0 if json['year'] is None else int(json['year'])

    def get_doi(self):
        return self.doi

    def get_coins(self):
        return self.coins

    def get_full_citation(self):
        return self.full_citation

    def get_normalized_score(self):
        return self.normalized_score

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.doi.get_identifier()

    def __clean_html(self, raw_html):
        regex = re.compile('<.*?>')
        return re.sub(regex,'',raw_html)


