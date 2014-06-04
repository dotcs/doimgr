import sys
import os
import httplib2
import urllib.request as urllib2
import logging

class Downloader(object):
    def __init__(self):
        self.filepath = None

    def get_filepath(self):
        return self.filepath

    def download(self, url, path, fallback_filename):
        logging.debug("Downloading URL {}".format(url))
        try:
            remotefile = urllib2.urlopen(url)
        except URLError:
            logging.error("URL could not be opened. Aborting.")
            return None
        filename = remotefile.info()['Content-Disposition']
        if filename is None:
            filename = fallback_filename
        logging.debug("Filename is {}".format(filename))

        self.filepath = os.path.join(path, filename)
        CHUNK = 16 * 1024
        with open(self.filepath, "wb") as fp:
            while True:
                chunk = remotefile.read(CHUNK)
                if not chunk: break
                fp.write(chunk)

        return self.filepath
