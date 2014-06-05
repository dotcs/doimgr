import os
import sys
import logging

from lib.search.request import Request

class API(object):
    API_BASEPATH = os.path.join(os.path.dirname(__file__), '..', 'API')
    TYPE_TYPES = 'types'
    TYPE_STYLES = 'styles'

    def __init__(self):
        pass

    def rebuild_valid_identifier(self, type_, path=None):
        valid_types = (self.TYPE_TYPES, self.TYPE_STYLES)
        if type_ not in valid_types:
            raise ValueError("Type {} is not valid. Valid types are {}".format(
                type_, valid_types))

        req = Request()

        if path is None:
            if type_ == self.TYPE_TYPES:
                path = os.path.join(self.API_BASEPATH, 'types.txt')
                url = "http://{}/types".format(req.URL_API_BASE)
            elif type_ == self.TYPE_STYLES:
                path = os.path.join(self.API_BASEPATH, 'styles.txt')
                url = "http://{}/styles".format(req.URL_API_BASE)

        results = req._request(url)
        if type_ == self.TYPE_TYPES:
            identifier = sorted([i.get('id','') for i in results.get('items', ())])
        elif type_ == self.TYPE_STYLES:
            identifier = sorted(results.get('items', ()))
        with open(path, 'w') as f:
            for value in identifier:
                f.write("{}\n".format(value))
        return path

    def get_valid_types(self):
        path = os.path.join(self.API_BASEPATH, 'types.txt')
        return self.__get_valid_API_values_from_file(path)

    def get_valid_styles(self):
        path = os.path.join(self.API_BASEPATH, 'styles.txt')
        return self.__get_valid_API_values_from_file(path)

    def __get_valid_API_values_from_file(self, filepath, format='plain'):
        """
        Method to derive valid API identifiers.

        @return: (list) valid API identifiers

        """
        if format == 'plain':
            with open(filepath, 'r') as f:
                result = f.read().split('\n')
            return result
        raise ValueError('Format {} is not implemented'.format(format))
