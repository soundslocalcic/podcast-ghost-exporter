"""
Buzzsprout player.

.. currentmodule:: ghostexporter.contrib.buzzsprout.player_embeds
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""


from ghostexporter import playback
import re


ENCLOSURE_PATTERN = re.compile(
    r"^https?://.*\.buzzsprout\.com/(?P<podcast>\d+)/(?:episodes/)?(?P<episode>\d+)"
)


@playback.register()
class BuzzsproutEmbed(playback.EmbedBase):
    """Buzzsprout player embed."""

    domains = ("*.buzzsprout.com",)

    def get_embed_url(self, url):
        """Return the iframe URL for a given audio file URL."""
        if match := ENCLOSURE_PATTERN.search(url):
            return "https://www.buzzsprout.com/%s/%s?iframe=true" % (
                match.groups()
            )
