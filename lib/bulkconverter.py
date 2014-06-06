import sys
import os
import logging

from lib.search.request import Request

class BulkConverter():
    def __init__(self):
        self.input_file = None
        self.output_file = None

    def run(self, in_, out_, style):
        logging.info('Starting with bulk convertation.')

        req = Request()

        for line in in_.readlines():
            if line.startswith('#'):
                continue
            identifier = line.strip()
            logging.info('Converting DOI: {}'.format(identifier))
            result = req.citation(req.prepare_citation_query(
                identifier), style=style)
            out_.write("{}\n".format(result))

        return True
