import os
import sys

class DOIError(Exception):
    pass

class DOI(object):
    """
    Representation of a DOI object.

    """
    URL_PROTOCOL = "http"
    URL_DOMAIN   = "dx.doi.org"

    def __init__(self, identifier):
        self.identifier = self.__parse_DOI_identifier(identifier)
        self.url = self.__generate_DOI_URL(self.identifier)

    def __parse_DOI_identifier(self, identifier):
        if identifier.startswith("http"):
            #raise DOIError("DOI identifier cannot be URLs!")
            return identifier[len("{}://{}/".format(self.URL_PROTOCOL, \
                self.URL_DOMAIN)):]
        return identifier

    def __generate_DOI_URL(self, identifier):
        return "{}://{}/{}".format(self.URL_PROTOCOL, self.URL_DOMAIN, \
                identifier)

    def get_URL(self):
        return self.url

    def get_identifier(self):
        return self.identifier
