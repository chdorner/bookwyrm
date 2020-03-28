''' functionality outline for a book data connector '''
from abc import ABC, abstractmethod

from fedireads import models


class AbstractConnector(ABC):
    ''' generic book data connector '''

    def __init__(self, identifier):
        # load connector settings
        info = models.Connector.objects.get(identifier=identifier)
        self.model = info

        self.url = info.base_url
        self.covers_url = info.covers_url
        self.search_url = info.search_url
        self.key_name = info.key_name
        self.max_query_count = info.max_query_count


    def is_available(self):
        ''' check if you're allowed to use this connector '''
        if self.model.max_query_count is not None:
            if self.model.query_count >= self.model.max_query_count:
                return False
        return True


    def has_attr(self, obj, key):
        ''' helper function to check if a model object has a key '''
        try:
            return hasattr(obj, key)
        except ValueError:
            return False


    @abstractmethod
    def search(self, query):
        ''' free text search '''
        # return list of search result objs
        pass


    @abstractmethod
    def get_or_create_book(self, book_id):
        ''' request and format a book given an identifier '''
        # return book model obj
        pass


    @abstractmethod
    def get_or_create_author(self, book_id):
        ''' request and format a book given an identifier '''
        # return book model obj
        pass


    @abstractmethod
    def update_book(self, book_obj):
        ''' sync a book with the canonical remote copy '''
        # return book model obj
        pass


class SearchResult(object):
    ''' standardized search result object '''
    def __init__(self, title, key, author, year, raw_data):
        self.title = title
        self.key = key
        self.author = author
        self.year = year
        self.raw_data = raw_data

    def __repr__(self):
        return "<SearchResult key={!r} title={!r} author={!r}>".format(
            self.key, self.title, self.author)
