import unittest
import json

from lib.search.result import SearchResult

class TestResponse(unittest.TestCase):
    def setUp(self):
        self.search_result_json = """{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"subtitle":[],"issued":{"date-parts":[[null]]},"score":1.0,"prefix":"none","author":[{"family":"Fabricius","given":"Maximilian"},{"family":"Saglia","given":"Roberto"},{"family":"Drory","given":"Niv"},{"family":"Fisher","given":"David"},{"family":"Bender","given":"Ralf"},{"family":"Hopp","given":"Ulrich"},{"family":"Debattista","given":"Victor P."},{"family":"Popescu","given":"C. C."}],"container-title":[],"reference-count":0,"deposited":{"date-parts":[[2014,3,6]],"timestamp":1394064000000},"title":["Velocity Dispersions Across Bulge Types"],"type":"proceedings-article","DOI":"10.1063\/1.3458497","URL":"http:\/\/dx.doi.org\/10.1063\/1.3458497","source":"CrossRef","publisher":"AIP","indexed":{"date-parts":[[2014,5,19]],"timestamp":1400474398092}}}"""
        self.search_result_json_huge_title = """{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"subtitle":[],"subject":["Space and Planetary Science","Astronomy and Astrophysics"],"issued":{"date-parts":[[2013,2,1]]},"score":1.0,"prefix":"http:\/\/id.crossref.org\/prefix\/10.1088","author":[{"family":"Jardel","given":"John R."},{"family":"Gebhardt","given":"Karl"},{"family":"Fabricius","given":"Maximilian H."},{"family":"Drory","given":"Niv"},{"family":"Williams","given":"Michael J."}],"container-title":["ApJ","The Astrophysical Journal"],"reference-count":68,"page":"91","deposited":{"date-parts":[[2013,1,14]],"timestamp":1358121600000},"issue":"2","title":["MEASURING DARK MATTER PROFILES NON-PARAMETRICALLY IN DWARF SPHEROIDALS: AN APPLICATION TO DRACO"],"type":"journal-article","DOI":"10.1088\/0004-637x\/763\/2\/91","ISSN":["0004-637X","1538-4357"],"URL":"http:\/\/dx.doi.org\/10.1088\/0004-637x\/763\/2\/91","source":"CrossRef","publisher":"IOP Publishing","indexed":{"date-parts":[[2014,5,21]],"timestamp":1400686024033},"volume":"763"}}"""

    def test_parse_json(self):
        res = SearchResult()
        try:
            res.parse_json(json.loads(self.search_result_json).get('message'))
        except Exception:
            self.fail("Valid JSON could not be parsed correctly")

    def test_parse_json_validate_results(self):
        res = SearchResult()
        res.parse_json(json.loads(self.search_result_json).get('message'))
        self.assertEqual(res.get_doi().get_identifier(),
                "10.1063/1.3458497")
        self.assertEqual(res.get_score(), 1.0)
        self.assertEqual(res.get_title(), 'Velocity Dispersions Across \
Bulge Types')
        self.assertEqual(res.get_year(), 0)
        self.assertEqual(res.get_authors(), 'Fabricius, Maximilian; \
Saglia, Roberto; Drory, Niv et al.')
        self.assertEqual(res.get_type(), 'proceedings-article')
        self.assertEqual(res.get_publisher(), 'AIP')
        self.assertEqual(res.get_url(), 'http://dx.doi.org/10.1063/1.3458497')

    def test_parse_json_check_title_format(self):
        res = SearchResult()
        res.parse_json(
                json.loads(self.search_result_json_huge_title).get('message') )
        self.assertEqual(res.get_title(), "Measuring Dark Matter Profiles \
Non-parametrically In Dwarf Spheroidals: An Application To Draco")

    def test_parse_json_with_unknown_title(self):
        res = SearchResult()
        j = json.loads(self.search_result_json).get('message')
        j['title'] = ''
        res.parse_json(j)
        self.assertEqual(res.get_title(), res.UNKNOWN_TITLE)

    def test_parse_json_with_unknown_year(self):
        res = SearchResult()
        j = json.loads(self.search_result_json_huge_title).get('message')
        j['issued'] = []
        res.parse_json(j)
        self.assertEqual(res.get_year(), res.UNKNOWN_YEAR)

    def test_parse_json_with_unknown_authors(self):
        res = SearchResult()
        j = json.loads(self.search_result_json_huge_title).get('message')
        j['author'] = []
        res.parse_json(j)
        self.assertEqual(res.get_authors(), res.UNKNOWN_AUTHORS)
