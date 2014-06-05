import unittest

from lib.filter import Filters

class TestDOI(unittest.TestCase):
    def setUp(self):
        self.valid_doi = "10.1063/1.3458497"
        self.valid_doi_with_protocol = "http://dx.doi.org/10.1063/1.3458497"
        self.invalid_doi = "a10.1063/1.3458497"
        self.valid_doi_organization = "10.1000"

    def test_add_valid_doi_filter(self):
        f = Filters()
        try:
            f.add('doi', self.valid_doi)
        except Exception:
            self.fail("Valid DOI could not be added")
        self.assertEqual(f.get_formatted_filters(), "doi:10.1063/1.3458497")

    def test_add_invalid_doi_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'doi', self.invalid_doi)

    def test_add_valid_from_pub_date_filter(self):
        f = Filters()
        try:
            f.add('from-pub-date', '2013')
            f.add('from-pub-date', '2013-02')
            f.add('from-pub-date', '2013-02-10')
        except Exception:
            self.fail("Valid DOI could not be added")
        self.assertEqual(f.get_formatted_filters(), "from-pub-date:2013-02-10")

    def test_add_invalid_from_pub_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'from-pub-date', "20132")

    def test_add_valid_has_funder_filter(self):
        f = Filters()
        try:
            f.add('has-funder', True)
        except Exception:
            self.fail("Valid has-funder could not be added")
        # use lower() since "True" and "False" are written with capital first
        # letters
        self.assertEqual(f.get_formatted_filters().lower(),
                "has-funder:true".lower())

    def test_add_invalid_has_funder_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'has-funder', "true")

    def test_empty_filter(self):
        f = Filters()
        self.assertEqual(f.get_formatted_filters(), "")

    def test_multiple_filter_entries(self):
        f = Filters()
        f.add('doi', self.valid_doi)
        f.add('from-pub-date', '2013')
        for entry in f.get_formatted_filters().split(','):
            self.assertIn(entry, ["doi:10.1063/1.3458497",
                "from-pub-date:2013"])

if __name__ == "__main__":
    unittest.main()
