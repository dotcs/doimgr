import os
import sys
import re

class DOI(object):
    """
    Representation of a DOI object.

    """
    URL_PROTOCOL = "http"
    URL_DOMAIN   = "dx.doi.org"

    UNKNOWN_IDENTIFIER = 'unknown_identifier'

    def __init__(self, identifier=None):
        self.identifier = self.UNKNOWN_IDENTIFIER
        self.url = None

        if identifier is not None:
            self.identifier = self.__parse_DOI_identifier(identifier)
            self.url = self.__generate_DOI_URL(self.identifier)

    def __parse_DOI_identifier(self, identifier):
        if not self.__is_valid_doi(identifier):
            raise ValueError("DOI is invalid. Given DOI: \
{}".format(identifier))
        if identifier.startswith("http"):
            #raise DOIError("DOI identifier cannot be URLs!")
            return identifier[len("{}://{}/".format(self.URL_PROTOCOL, \
                self.URL_DOMAIN)):]
        return identifier

    def __is_valid_doi(self, identifier):
        regex = re.compile("(http\:\/\/dx\.doi\.org/)?10\.[\d\.]+(/*)?")
        return regex.match(identifier) is not None

    def __generate_DOI_URL(self, identifier):
        return "{}://{}/{}".format(self.URL_PROTOCOL, self.URL_DOMAIN, \
                identifier)

    def get_URL(self):
        return self.url

    def get_identifier(self):
        return self.identifier
