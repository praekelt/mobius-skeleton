from haystack import indexes

from search.base_search_indexes import IndexMixin
from models import TrivialContent


class TrivialContentIndex(IndexMixin, indexes.Indexable):
    model = TrivialContent

