"""
Podacst player library module.

.. currentmodule:: ghostexporter.playback.library
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from ghostexporter.settings import USER_AGENT
from urllib.parse import urlparse
import re
import requests


TRACKING_PREFIXES = (
    "chrt.fm",
    "chtbl.com",
    "claritaspod.com",
    "*.gum.fm",
    "mgln.ai",
    "op3.dev",
    "p.podderapp.com",
    "*.podtrac.com",
    "pdcds.co",
    "pdcn.co",
    "pdrl.fm",
    "pdst.fm",
    "prfx.byspotify.com",
    "pscrb.fm",
    "swap.fm"
)


class EmbedBase(object):
    """Base embed class."""

    def apply(self, url):
        """Determine whether this player can resolve the given URL."""
        if domains := getattr(self, "domains", None):
            enclosure_domain = urlparse(url).netloc

            for domain in domains:
                ex = domain.replace("*", ".*")

                if re.match(ex, enclosure_domain) is not None:
                    return True

            return False

        raise NotImplementedError  # pragma: no cover

    def get_embed_url(self, url):
        """Return the embed URL for a given audio file."""
        raise NotImplementedError  # pragma: no cover

    def get_embed_html(self, url):
        """Return a player's iframe code given a audio file URL."""
        if iframe_url := self.get_embed_url(url):
            return (
                '<iframe src="%s" width="100%%" height="180" frameborder="0" scrolling="no" seamless></iframe>'  # noqa
            ) % iframe_url


class Library(object):
    """Player embed library."""

    def __init__(self):
        """Initialise the library."""
        self.__players = []

    def register(self, parser):
        """Register a player class with the library."""
        self.__players.append(parser)

    def is_tracking_url(self, url):
        """Return whether a URL has a tracking prefix."""
        domain = urlparse(url).netloc
        for prefix_domain in TRACKING_PREFIXES:
            pattern = r"^(?:www\.)?" + prefix_domain.replace(
                ".", "\\."
            ).replace(
                "*\\.",
                "(?:[^\\.]+\\.)?"
            ) + "$"

            match = re.search(pattern, domain)

            if match is not None:
                return True

        return False

    def strip_tracking(self, url):
        """Remove tracking prefixes from URLs."""
        while self.is_tracking_url(url):
            response = requests.head(
                url,
                headers={
                    "User-Agent": USER_AGENT
                }
            )

            if response.status_code not in (301, 302):
                break

            url = response.headers["Location"]

        return url

    def get_html(self, enclosure):
        """Return an HTML string for a given audio file URL."""
        enc = self.strip_tracking(enclosure)

        for Player in self.__players:
            player = Player()
            if player.apply(enc):
                if html := player.get_embed_html(enc):
                    return html
