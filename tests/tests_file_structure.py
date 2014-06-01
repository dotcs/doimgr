import unittest
import os
import sys

class TestFileStructure(unittest.TestCase):
    def test_styles_file_exists(self):
        self.assertTrue(os.path.isfile(os.path.join('API', 'styles.txt')))
