import unittest

from lib.search.request import Request
from lib.doi import DOI

class TestRequest(unittest.TestCase):
    def setUp(self):
        self.req = Request()

    def test_prepare_search_query(self):
        result = self.req.prepare_search_query("Maximilian Fabricius !Solar")
        result_enties = result.split('&')
        awaited_result_entries = [
                'rows=20', 
                'order=desc', 
                'sort=score',
                'query=Maximilian+Fabricius+%21Solar',
                'filter='
        ]
        for entry in result_enties:
            self.assertIn(entry, awaited_result_entries)

    def test_prepare_search_query_with_different_rows_settings(self):
        result = self.req.prepare_search_query("Maximilian Fabricius !Solar",
                rows=10)
        result_enties = result.split('&')
        awaited_result_entries = [
                'rows=10', 
                'order=desc', 
                'sort=score',
                'query=Maximilian+Fabricius+%21Solar',
                'filter='
        ]
        for entry in result_enties:
            self.assertIn(entry, awaited_result_entries)

    def test_prepare_search_query_with_different_sort_settings(self):
        result = self.req.prepare_search_query("Maximilian Fabricius !Solar",
                sort='published')
        result_enties = result.split('&')
        awaited_result_entries = [
                'rows=20', 
                'order=desc', 
                'sort=published',
                'query=Maximilian+Fabricius+%21Solar',
                'filter='
        ]
        for entry in result_enties:
            self.assertIn(entry, awaited_result_entries)

    def test_prepare_search_query_with_different_year_settings(self):
        result = self.req.prepare_search_query("Maximilian Fabricius !Solar",
                year=2006)
        result_enties = result.split('&')
        awaited_result_entries = [
                'rows=20', 
                'order=desc', 
                'sort=score',
                'query=Maximilian+Fabricius+%21Solar',
                'filter=from-pub-date%3A2006'
        ]
        for entry in result_enties:
            self.assertIn(entry, awaited_result_entries)

    def test_prepare_search_query_sort_values(self):
        for method in ('score', 'updated', 'deposited', 'indexed', 'published'):
            try:
                result = self.req.prepare_search_query("Maximilian Fabricius \
!Solar", sort=method)
            except Exception:
                self.fail("Not all valid sort strings are possible")

        for method in ('arbitrary', 'invalid'):
            self.assertRaises(ValueError, self.req.prepare_search_query,
                    "Maximilian Fabricius !Solar", sort=method)

    def test_prepare_search_query_order_values(self):
        for method in ('asc', 'desc'):
            try:
                result = self.req.prepare_search_query("Maximilian Fabricius \
!Solar", order=method)
            except Exception:
                self.fail("Not all valid sort strings are possible")

        for method in ('arbitrary', 'invalid'):
            self.assertRaises(ValueError, self.req.prepare_search_query,
                    "Maximilian Fabricius !Solar", order=method)

    def test_prepare_citation_query_valid_DOI(self):
        valid_doi_identifier = "10.1063/1.3458497"
        self.assertEqual(self.req.prepare_citation_query(valid_doi_identifier),
                "10.1063/1.3458497/transform")
