import os
import sys
import logging
import re

class Validator(object):

    UNKNOWN   = 0
    BOOLEAN   = 1
    INTEGER   = 2
    STRING    = 3
    DATE      = 4
    FUNDER_ID = 5
    MEMBER_ID = 6
    URL       = 7
    MIME_TYPE = 8
    ORCID     = 9
    ISSN      = 10
    TYPE      = 11
    DIRECTORY = 12
    DOI       = 13

    def __init__(self):
        pass

    def __get_valid_values(self):
        valid_values = [
            ('has-funder'               , self.BOOLEAN   ),
            ('funder'                   , self.FUNDER_ID ),
            ('prefix'                   , self.MEMBER_ID ),
            ('member'                   , self.DATE      ),
            ('from-index-date'          , self.DATE      ),
            ('until-index-date'         , self.DATE      ),
            ('from-deposition-date'     , self.DATE      ),
            ('until-deposition-date'    , self.DATE      ),
            ('from-frist-deposit-date'  , self.DATE      ),
            ('until-first-deposit-date' , self.DATE      ),
            ('from-pub-date'            , self.DATE      ),
            ('until-pub-date'           , self.DATE      ),
            ('has-license'              , self.BOOLEAN   ),
            ('license.url'              , self.URL       ),
            ('license.version'          , self.STRING    ),
            ('license.delay'            , self.INTEGER   ),
            ('has-full-text'            , self.BOOLEAN   ),
            ('full-text.version'        , self.STRING    ),
            ('full-text.type'           , self.MIME_TYPE ),
            ('public-references'        , self.UNKNOWN   ),
            ('has-references'           , self.BOOLEAN   ),
            ('has-archive'              , self.BOOLEAN   ),
            ('archive'                  , self.STRING    ),
            ('has-orcid'                , self.BOOLEAN   ),
            ('orcid'                    , self.ORCID     ),
            ('issn'                     , self.ISSN      ),
            ('type'                     , self.TYPE      ),
            ('directory'                , self.DIRECTORY ),
            ('doi'                      , self.DOI       ),
            ('updates'                  , self.DOI       ),
            ('is-update'                , self.BOOLEAN   ),
            ('has-update-policy'        , self.BOOLEAN   ),
        ]
        return valid_values

    def is_valid(self, key, value):
        valid_values = self.__get_valid_values()
        if key not in [v[0] for v in valid_values]:
            raise ValueError("Key {} is invalid an cannot be added to the \
filter list.".format(key))

        for k, t in valid_values:
            if k == key:
                if not self.__is_valid(value, t):
                    return False
                return True
        return False

    def __is_valid(self, value, type_):
        if type_ in (self.UNKNOWN, self.DIRECTORY):
            logging.debug("Datatype handling is unkown. Assuming it is valid.")
            return True
        elif type_ == self.BOOLEAN:
            return type(value) is type(True)
        elif type_ == self.INTEGER:
            return type(value) == type(0)
        elif type_ == self.STRING:
            return type(value) == type("string")
        elif type_ == self.DATE:
            if type(value) == type(0):
                # convert to string if necessary
                value = str(value)
            regex = re.compile("^\d{4}((-\d{2}){1,2})?$")
            return regex.match(value) is not None
        elif type_ == self.URL:
            return type(value) == type("string") and value.startswith('http://')
        elif type_ == self.MIME_TYPE:
            regex = re.compile("^.+/.+$")
            return regex.match(value) is not None
        elif type_ == self.ORCID:
            regex = re.compile("(http\:\/\/orcid\.org/)?\d{4}-\d{4}-\d{4}-\d{4}")
            return regex.match(value) is not None
        elif type_ == self.ISSN:
            regex = re.compile("^.{4}-.{4}$")
            return regex.match(value) is not None
        elif type_ == self.TYPE:
            # TODO: Wed Jun  4 21:04:32 CEST 2014, @fabi, comment:
            # implementation missing
            raise NotImplemented("Sanity check needs to be implemented")
        elif type_ in (self.DOI, self.FUNDER_ID, self.MEMBER_ID):
            regex = re.compile("(http\:\/\/dx\.doi\.org/)?10\.[\d\.]+(/*)?")
            return regex.match(value) is not None
