"""
Transistor player.

.. currentmodule:: ghostexporter.contrib.transistor.player_embeds
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""


from ghostexporter import playback
import re


@playback.register()
class TransistorEmbed(playback.EmbedBase):
    """Transistor player embed."""

    domains = ("media.transistor.fm",)

    def get_embed_url(self, url):
        """Return the iframe URL for a given audio file URL."""
        return re.sub(
            r"^https?://media\.transistor\.fm/([^/]+)/[^\.]+\.mp3$.*",
            r"https://share.transistor.fm/e/\g<1>",
            url
        )
