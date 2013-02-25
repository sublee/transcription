# -*- coding: utf-8 -*-
"""
    transcription.representation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Symbolic linguistic representation model.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import re

from typequery import GenericMethod
import yaml

from .respell import Respell


__all__ = ['Representation', 'generate_from_yaml']


class Representation(object):
    """A class for `symbolic linguistic representation`_. One of representation
    can respell a text to another representation if the respelling pipeline
    is defined.

    >>> de_ipa_underlying = Representation('de.ipa.underlying')
    >>> ko_orthography_hang = Representation('ko.orthography.hang')
    >>> print de_ipa_underlying.respell('ʃrˈødɪnɡɛr', ko_orthography_hang)
    슈뢰딩거

    .. _symbolic linguistic representation:
       http://en.wikipedia.org/wiki/Symbolic_linguistic_representation
    """

    name = None
    locale = None
    vars = None
    respellings = None

    def __init__(self, name, locale=None, vars=None, respellings=None):
        self.name = name
        self.locale = locale
        self.vars = vars or {}
        self.respellings = respellings or {}

    def respell(self, dest, text):
        for respell in self.respellings[dest]:
            text = respell(text)
        return text

    def respellables(self):
        return self.respellings.keys()


class RepresentationGenerator(object):

    _ref_pattern = re.compile(r'^<(.+)>$')
    _respell_pattern = re.compile(r'^respell->(.+)$')

    normalize_glyphs = GenericMethod('normalize_glyphs')

    @normalize_glyphs.of(basestring)
    def normalize_glyphs(val):
        return [unicode(val)]

    @normalize_glyphs.of(dict)
    def normalize_glyphs(val):
        assert len(val) == 1
        assert val.values()[0] is None
        return list(unicode(val.keys()[0]))

    @normalize_glyphs.of(list, with_receiver=True)
    def normalize_glyphs(normalize_glyphs, vals, flatten=None):
        if flatten is None:
            flatten = []
        for val in vals:
            if isinstance(val, list):
                normalize_glyphs(val, flatten)
            else:
                flatten.extend(normalize_glyphs(val))
        return flatten

    def resolve_refs(self, glyphs, vars, var=None):
        has_ref = False
        resolved  = []
        for glyph in glyphs:
            ref_match = self._ref_pattern.match(glyph)
            if ref_match is None:
                resolved.append(glyph)
                continue
            ref = ref_match.group(1)
            has_ref = True
            if var == ref:
                continue
            try:
                resolved.extend(self.resolve_refs(vars[ref],
                                                  vars, var))
            except ValueError:
                resolved.extend(vars[ref])
        if not has_ref:
            raise ValueError('The glyphs doesn\'t have references')
        return resolved

    def generate_from_yaml(self, stream):
        data = yaml.load(stream)
        try:
            name = data['name']
        except KeyError:
            raise ValueError('Representation needs a name')
        locale = data.get('locale')
        # vars
        vars = {}
        for var, definition in data.get('define', {}).iteritems():
            glyphs = self.normalize_glyphs(definition)
            assert isinstance(glyphs, list)
            vars[var] = glyphs
        for var, glyphs in vars.iteritems():
            try:
                vars[var] = self.resolve_refs(glyphs, vars, var)
            except ValueError:
                continue
        # respelling pipelines
        respellings = {}
        for key, val in data.iteritems():
            respell_match = self._respell_pattern.match(key)
            if respell_match is None:
                continue
            dest = respell_match.group(1)
            raw_pipeline = (item.items()[0] for item in val)
            respellings[dest] = [Respell(pattern, replacement, vars)
                                 for pattern, replacement in raw_pipeline]
        return Representation(name, locale, vars, respellings)


generate_from_yaml = RepresentationGenerator().generate_from_yaml
