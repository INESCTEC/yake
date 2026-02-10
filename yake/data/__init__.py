"""Data representation module for keyword extraction!"""

from .composed_word import ComposedWord
from .core import DataCore
from .single_word import SingleWord

__all__ = ["DataCore", "SingleWord", "ComposedWord"]
