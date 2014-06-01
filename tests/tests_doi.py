import unittest

from lib.doi import DOI

class TestDOI(unittest.TestCase):
    def setUp(self):
        self.valid_doi = "10.1063/1.3458497"
        self.valid_doi_with_protocol = "http://dx.doi.org/10.1063/1.3458497"
        self.invalid_doi = "a10.1063/1.3458497"
        self.valid_doi_organization = "10.1000"

    def test_set_identifier_on_creation(self):
        try:
            doi = DOI(self.valid_doi)
            doi = DOI(self.valid_doi_organization)
        except Exception:
            self.fail("Creation of DOI object failed")

    def test_set_no_identifier_on_creation(self):
        try:
            doi = DOI()
        except Exception:
            self.fail("Creation of DOI object failed")

    def test_set_invalid_identifier_on_creation(self):
        self.assertRaises(ValueError, DOI, self.invalid_doi)

    def test_query_url_of_undefined_doi_object(self):
        doi = DOI()
        self.assertEqual(doi.get_URL(), None)

    def test_query_url_of_undefined_doi_object(self):
        doi = DOI()
        self.assertEqual(doi.get_identifier(), doi.UNKNOWN_IDENTIFIER)

    def test_query_url_of_doi_object(self):
        doi = DOI(self.valid_doi)
        self.assertEqual(doi.get_URL(), "http://dx.doi.org/10.1063/1.3458497")
        self.assertEqual(doi.get_identifier(), "10.1063/1.3458497")

    def test_query_url_of_doi_object_with_protocol(self):
        doi = DOI(self.valid_doi_with_protocol)
        self.assertEqual(doi.get_URL(), "http://dx.doi.org/10.1063/1.3458497")
        self.assertEqual(doi.get_identifier(), "10.1063/1.3458497")

if __name__ == "__main__":
    unittest.main()
