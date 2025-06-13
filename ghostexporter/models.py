"""
This is where the business logic for the package lives.

.. currentmodule:: ghostexporter.models
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse as parse_date
from feedparser import parse as parse_feed
from hashlib import md5
from pickle import dumps
from slugify import slugify
from urllib.parse import quote
from .transformers import get_transformer
import bleach
import requests


ALLOWED_TAGS = [
    "p", "br", "strong", "b", "em", "i", "u", "blockquote",
    "ul", "ol", "li", "a", "code", "pre", "img", "h1", "h2", "h3",
    "h4", "h5", "h6", "hr", "figure", "figcaption", "iframe"
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "iframe": ["src", "width", "height", "frameborder", "allow"]
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


class ItemList(object):
    """List of feed items."""

    def __init__(self, url: str):
        """Initialise class with feed URL."""
        self.__url = url
        self.__cache = {}

    def get_feed(self):
        """Return a feedparser feed object."""
        response = requests.get(self.__url)
        response.raise_for_response()
        return parse_feed(response.content)

    def all(self):
        """Return a list of feed items."""
        if "all" not in self.__cache:
            feed = self.get_feed()
            items = []

            for entry in feed.entries:
                kwargs = {
                    "title": entry.get("itunes_title", entry.get("title")),
                    "summary": entry.get("summary", ""),
                    "published": parse_date(entry.published)
                }

                for content in entry.get("content", []):
                    if content.get("type") == "text/html":
                        kwargs["description"] = content["value"]

                if author := entry.get("author_detail"):
                    kwargs["author"] = author

                item = Item(**kwargs)
                items.append(item)

            items = sorted(items, key=lambda item: item.published)
            self.__cache["all"] = items

        return self.__cache["all"]

    def to(self, version: str):
        """Transform the feed item list to a given document format."""
        Transformer = get_transformer(version)
        transformer = Transformer(self.all)

        return transformer


class Feed(object):
    """Feed object, containing a list of items."""

    def __init__(self, url: str):
        """Initialise class with feed URL."""
        self.items = ItemList(url)


class Item(object):
    """Individiaul feed item."""

    def __init__(self, **kwargs):
        """Initialise item with keyword arguments."""
        self.created = datetime.now()
        data_serialised = []

        for key in sorted(kwargs.keys()):
            value = kwargs[key]
            data_serialised.append(
                "%s=%s" % (
                    quote(key),
                    quote(dumps(value))
                )
            )

        data_serialised = "&".join(data_serialised)
        hashed = md5(data_serialised.encode("utf-8")).hexdigest()

        try:
            self.title = kwargs.pop("title")
            self.summary = kwargs.pop("summary", "")
            self.published = kwargs.pop("published")
            description = kwargs.pop("description", "")
            self.author = kwargs.pop("author", {})
        except KeyError as ex:
            raise TypeError("%s is required." % ex.args)

        for key in kwargs.keys():
            raise TypeError("Invalid argument: '%s'" % key)

        html = bleach.clean(
            description,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
            strip_comments=True
        )

        soup = BeautifulSoup(html, "html.parser")

        self.id = hashed
        self.description = str(soup)
        self.slug = slugify(self.title)
