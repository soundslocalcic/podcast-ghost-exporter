"""
Base classes for document conversion.

.. currentmodule:: ghostexporter.transformers.base
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from collections import defaultdict
from datetime import datetime
import json


class ItemsHook(object):
    """
    Item hook.

    Used to curry the callable that returns
    an iterable of items that need to be transformed.
    """

    def __init__(self, items_getter: callable, item_transformer: callable):
        """
        Class initialiser.

        Initialise the hook with the function used to return items,
        and the function used to transform individual items.
        """
        self.__hook = items_getter
        self.__transformer = item_transformer

    def transform(self):
        """Transform individual items obtained via the getter."""
        for item in self.__hook():
            yield self.__transformer(item)


class TransformerBase(object):
    """Base transformer."""

    def __init__(self, items_callabke: callable):
        """Initialise with an iterable to get feed items."""
        self.items_hook = ItemsHook(
            items_callabke,
            self.transform_item
        )

    def transform_items(self, item_hook: callable):
        """Create a document that will contain items."""
        raise NotImplementedError  # pragma: no cover

    def transform_item(self, item):
        """Create a document that contains an individual item."""
        raise NotImplementedError  # pragma: no cover


class GhostEncoder(json.JSONEncoder):
    """JSON encoder for streaming feed items and handling dates."""

    def default(self, value):
        """Handle streamable content and transform dates."""
        if isinstance(value, ItemsHook):
            collections = defaultdict(list)
            for item in value.transform():
                for collection, docs in item.items():
                    collections[collection].extend(docs)

            return collections

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


class JSONTransformer(TransformerBase):
    """Base JSON transformer."""

    def write(self, stream):
        """Transform the feed items and write to a stream."""
        json.dump(
            self.transform_items(self.items_hook),
            stream,
            cls=GhostEncoder
        )
