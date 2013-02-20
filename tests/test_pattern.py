# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from transcription import Pattern


def test_tokenize():
    p = Pattern('a(b|,c,d|e)c')
    assert p.tokens == ('a', (('b', ''), ('c',), ('d', 'e')), 'c')
    assert p.possibles() == \
           [(0, 'abc'), (0, 'ac'), (1, 'acc'), (2, 'adc'), (2, 'aec')]


def test_brian():
    # 위계 -- 2012-04-20
    p = Pattern('(y,wi).g(j,)e')
    assert p.tokens == ((('y',), ('wi',)), '.g', (('j',), ('',)), 'e')
    assert p.possibles() == \
           [(0, 'y.gje'), (1, 'y.ge'), (1, 'wi.gje'), (2, 'wi.ge')]
