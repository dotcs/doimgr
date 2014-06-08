import unittest

from lib.filter import Filters

class TestDOI(unittest.TestCase):
    def setUp(self):
        self.valid_doi = "10.1063/1.3458497"
        self.valid_doi_with_protocol = "http://dx.doi.org/10.1063/1.3458497"
        self.invalid_doi = "a10.1063/1.3458497"
        self.valid_doi_organization = "10.1000"

    #### DOI TESTS

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

    #### DATE TESTS

    def _test_valid_date_filter(self, filtername, date, awaited_result):
        f = Filters()
        try:
            f.add(filtername, date)
        except Exception:
            self.fail("Valid date could not be added: {}".format(filtername))
        self.assertEqual(f.get_formatted_filters(), awaited_result)

    def test_add_valid_from_pub_date_filter(self):
        for date in ('2013', '2013-02', '2013-02-10'):
            self._test_valid_date_filter('from-pub-date', date, 
                "{}:{}".format('from-pub-date', date))

    def test_add_invalid_from_pub_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'from-pub-date', "20132")

    def test_add_valid_from_index_date_filter(self):
        for date in ('2013', '2013-02', '2013-02-10'):
            self._test_valid_date_filter('from-index-date', date, 
                "{}:{}".format('from-index-date', date))

    def test_add_invalid_from_index_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'from-index-date', "20132")

    def test_add_valid_until_index_date_filter(self):
        for date in ('2013', '2013-02', '2013-02-10'):
            self._test_valid_date_filter('until-index-date', date, 
                "{}:{}".format('until-index-date', date))

    def test_add_invalid_until_index_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'until-index-date', "20132")

    def test_add_valid_from_deposition_date_filter(self):
        for date in ('2013', '2013-02', '2013-02-10'):
            self._test_valid_date_filter('from-deposition-date', date, 
                "{}:{}".format('from-deposition-date', date))

    def test_add_invalid_from_deposition_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'from-deposition-date', "20132")

    def test_add_valid_until_deposition_date_filter(self):
        for date in ('2013', '2013-02', '2013-02-10'):
            self._test_valid_date_filter('until-deposition-date', date, 
                "{}:{}".format('until-deposition-date', date))

    def test_add_invalid_until_deposition_date_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'until-deposition-date', "20132")

    ### BOOLEAN FILTER TESTS

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

    ### URL TESTS

    def test_add_valid_license_url_filter(self):
        f = Filters()
        try:
            f.add('license.url', 'http://example.com/this/is/a/test.html')
        except Exception:
            self.fail("Valid license.url could not be added")

    def test_add_invalid_license_url_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'license.url',
                'httpf://example.com/this/is/a/invalid/url.html')

    ### STRING TESTS

    def test_add_valid_full_text_version_filter(self):
        f = Filters()
        try:
            f.add('full-text.version', '1.01.beta')
        except Exception:
            self.fail("Valid full-text.version could not be added")

    def test_add_invalid_full_text_version_filter(self):
        f = Filters()
        self.assertRaises(ValueError, f.add, 'full-text.version', 4)

    ### OTHER TESTS

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
