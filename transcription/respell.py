# -*- coding: utf-8 -*-
"""
    transcription.respell
    ~~~~~~~~~~~~~~~~~~~~~

    Compiles a respelling DSL to a regular expression.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import re
from warnings import warn


class Respell(object):

    _vowel_var = 'vowels'
    _vowel_alias = '@'
    _var_pattern = re.compile(r'<(?P<name>[a-zA-Z_][a-zA-Z0-9_]+)>')

    def __init__(self, pattern, repl, vars):
        self.pattern = pattern
        self.repl = repl
        self.vars = vars

    @property
    def compiled_pattern(self):
        try:
            return self._compiled_pattern
        except AttributeError:
            pass
        self._compiled_pattern, self._compiled_repl = self._compile()
        return self._compiled_pattern

    @property
    def compiled_repl(self):
        try:
            return self._compiled_repl
        except AttributeError:
            pass
        self._compiled_pattern, self._compiled_repl = self._compile()
        return self._compiled_repl

    def _compile(self):
        pattern, repl = self.pattern, self.repl
        if repl is None:
            repl = ''
        # replace @ to <vowels>
        if self._vowel_alias in pattern:
            if self._vowel_var not in self.vars:
                warn('A pattern uses {!r} but there is no {!r} '
                     'variable'.format(self._vowel_var, self._vowel_var),
                     UserWarning)
            wrapped_vowel_var = self._wrap_var(self._vowel_var)
            pattern = pattern.replace(self._vowel_alias, wrapped_vowel_var)
        # inline variable references
        pattern = self._inline_vars(pattern)
        return (re.compile(pattern), repl)

    def _inline_vars(self, pattern, repl):
        def repl(match):
            var = match.group('name')
            try:
                glyphs = self.vars[var]
            except KeyError:
                warn('{!r} is not defined'.format(var), UserWarning)
                return r'.'
            return r'(?:{})'.format('|'.join(map(re.escape, glyphs)))
        return re.sub(self._var_pattern, repl, pattern)

    def _wrap_var(self, var):
        """``'var'`` to ``'<var>'``."""
        return ''.join(['<', var, '>'])

    def __call__(self, text):
        return re.sub(self.compiled_pattern, self.compiled_repl, text)

    def __repr__(self):
        return '{}({!r}, {!r}, vars=...)'.format(type(self).__name__,
                                                 self.pattern,
                                                 self.repl)
