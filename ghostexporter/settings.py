"""
Settings module.

.. currentmodule:: ghostexporter.settings
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from .version import __version__

USER_AGENT = "ghostexporter/%s" % __version__
PLUGINS = [
    "ghostexporter.contrib.buzzsprout",
    "ghostexporter.contrib.transistor"
]
