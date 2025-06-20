"""
A module for handling swappable podcast player embeds.

.. currentmodule:: ghostexporter.playback
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from ghostexporter import hooks, settings, utils
from importlib import import_module
from .library import EmbedBase, Library


embeds = Library()


def register():
    """Register a player class with the library."""

    def wrapper(cls):
        embeds.register(cls)
        return cls

    return wrapper


__all__ = (
    "EmbedBase",
    "embeds",
    "register"
)


@hooks.on("ready")
def ready():
    for plugin in settings.PLUGINS:
        name = '%s.player_embeds' % plugin

        try:
            import_module(name)
        except ImportError:
            if utils.module_has_submodule(plugin, "player_embeds"):
                raise  # pragma: no cover
