"""
Contains the v5 Ghost data transformer.

.. currentmodule:: ghostexporter.transformers.v5
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from datetime import datetime
from ghostexporter.playback import embeds
from .base import JSONTransformer
import json


class Ghost5Transformer(JSONTransformer):
    """v5 Ghost data transformer."""

    def build_content(self, item):
        """Return the HTML for the post."""
        html = []

        if iframe := embeds.get_html(item.enclosure):
            html.append(iframe)

        html.append(item.description)
        return "\n\n".join(html)

    def transform_items(self, item_hook: callable):
        """Create a Ghost document with metadata and item list."""
        now = datetime.now()
        timestamp = now.timestamp()

        return {
            "db": [
                {
                    "meta": {
                        "exported_on": int(timestamp * 1000),
                        "version": "5.125.0-0-g09f7924d"
                    },
                    "data": item_hook
                }
            ]
        }

    def get_lexical(self, item):
        """Return a Lexical document from an item."""
        return {
            "root": {
                "children": [
                    {
                        "type": "html",
                        "html": self.build_content(item),
                        "version": 1
                    }
                ],
                "type": "root"
            }
        }

    def transform_item(self, item):
        """Transform a feed item into a JSON object."""
        lexical = self.get_lexical(item)
        return {
            "posts": [
                {
                    "id": item.id,
                    "slug": item.slug,
                    "title": item.title,
                    "html": self.build_content(item),
                    "lexical": json.dumps(lexical),
                    "type": "post",
                    "status": "published",
                    "visibility": "public",
                    "created_at": item.created,
                    "published_at": item.published
                }
            ],
            "posts_authors": [
                {
                    "post_id": item.id,
                    "author_id": "1"
                }
            ]
        }
