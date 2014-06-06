import os
import sys
import logging

class Clipboard(object):
    @staticmethod
    def copy_to(string):
        logging.debug("Copying '{}' to the clipboard".format(string))

        if sys.platform == 'darwin':
            # Mac OS X
            os.system('echo "{}" | pbcopy'.format(string))
            return True

        logging.error('Copying to clipboard is not supported on your \
platform yet.')
        return False
