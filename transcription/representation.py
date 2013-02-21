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
    variables = None
    respelling_pipelines = None

    def __init__(self, name, locale=None,
                 variables=None, respelling_pipelines=None):
        self.name = name
        self.locale = locale
        self.variables = variables or {}
        self.respelling_pipelines = respelling_pipelines or {}


class RepresentationGenerator(object):

    ref_pattern = re.compile(r'^<(.+)>$')
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

    def resolve_refs(self, glyphs, variables, var=None):
        has_ref = False
        resolved  = []
        for glyph in glyphs:
            ref_match = self.ref_pattern.match(glyph)
            if ref_match is None:
                resolved.append(glyph)
                continue
            ref = ref_match.group(1)
            has_ref = True
            if var == ref:
                continue
            try:
                resolved.extend(self.resolve_refs(variables[ref],
                                                  variables, var))
            except ValueError:
                resolved.extend(variables[ref])
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
        variables = {}
        for var, definition in data.get('define', {}).iteritems():
            glyphs = self.normalize_glyphs(definition)
            assert isinstance(glyphs, list)
            variables[var] = glyphs
        # resolve variable references
        for var, glyphs in variables.iteritems():
            try:
                variables[var] = self.resolve_refs(glyphs, variables, var)
            except ValueError:
                continue
        return Representation(name, locale, variables)


generate_from_yaml = RepresentationGenerator().generate_from_yaml
