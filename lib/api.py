import os
import sys
import logging

from lib.search.request import Request

class API(object):
    API_BASEPATH = os.path.join(os.path.dirname(__file__), '..', 'API')

    def __init__(self):
        pass

    def rebuild_valid_types(self, path=None):
        if path is None:
            path = os.path.join(self.API_BASEPATH, 'types.txt')
        req = Request()
        url = "http://{}/types".format(req.URL_API_BASE)
        results = req._request(url)
        identifier = [i.get('id','') for i in results.get('items', ())]
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
