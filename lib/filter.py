import os
import sys

from lib.validator import Validator

class Filters(object):

    def __init__(self):
        self.filters = {}

    def add(self, key, value):
        v = Validator()
        if not v.is_valid(key, value):
            raise ValueError("Formatting for key {} is not valid.".format(key))
        self.filters[key] = value
        return self.filters

    def get_filters(self):
        return self.filters

    def get_formatted_filters(self):
        return ",".join(["{}:{}".format(key, value) for key, value in
            self.filters.items()])

