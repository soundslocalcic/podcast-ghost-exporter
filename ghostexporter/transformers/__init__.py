"""
Convenience module for finding transformers by version number.

.. currentmodule:: ghostexporter.transformers
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from .v5 import Ghost5Transformer


def get_transformer(version: str):
    """Return the transformer class matching the given version number."""
    return {
        "5": Ghost5Transformer
    }[version]
