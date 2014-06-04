import os
import sys

class FullTextURL(object):

    def __init__(self, url, license_url=None):
        self.url = url
        self.license_url = license_url

    def __str__(self):
        return "<FullText @ {}>".format(self.url)

    def get_url(self):
        return self.url

    def get_license_url(self):
        return self.license_url
