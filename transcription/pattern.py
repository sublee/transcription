# -*- coding: utf-8 -*-
"""
    transcription.pattern
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import re


__all__ = ['Pattern']


class Pattern(object):

    token_pattern = re.compile('(?:([^()]+)|\((.+?)\))')
    tokens = None

    def __init__(self, text):
        self.tokens = self.tokenize(text)

    def tokenize(self, text):
        """Tokenizes invariants or variants from a pronunciation."""
        if not isinstance(text, unicode):
            raise TypeError('\'text\' should be {}'.format(unicode.__name__))
        tokens = []
        for match in self.token_pattern.finditer(text):
            invariant, variant = match.groups()
            if invariant:
                token = invariant
            elif variant:
                ordered_candidates = variant.strip('()')
                token = tuple(tuple(candidates.split('|'))
                              for candidates in ordered_candidates.split(','))
            tokens.append(token)
        return tuple(tokens)

    def possibles(self):
        """Returns all possible pronunciations."""
        possibles = [(0, [])]
        for x, token in enumerate(self.tokens):
            # invariant
            if isinstance(token, unicode):
                for priority, buf in possibles:
                    buf.append(token)
                continue
            # variant
            new_possibles = []
            for priority, buf in possibles:
                for new_priority, candidates in enumerate(token, priority):
                    for candidate in candidates:
                        new_possibles.append((new_priority, buf + [candidate]))
            possibles = new_possibles
        return [(priority, ''.join(buf)) for priority, buf in possibles]
