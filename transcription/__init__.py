# -*- coding: utf-8 -*-
"""
    transcription
    ~~~~~~~~~~~~~

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from . import pattern, representation
from .pattern import Pattern
from .representation import Representation


__version__ = '0.0.0'
__all__ = [
    # submodules
    'pattern', 'representation',
    # Classes
    'Pattern', 'Representation',
]
