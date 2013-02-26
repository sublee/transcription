# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from transcription import Representation, representation


def test_parse_yaml(rep):
    assert isinstance(rep, Representation)


def test_vars(rep):
    assert rep.vars == {
        'vowels': list('aeiou'),
        'consonants': list('qwrtypsdfghjklzxcvbnm'),
        'long_vowels': list('AEIOU'),
        'all': list('aeiouqwrtypsdfghjklzxcvbnmAEIOU'),
        'self_ref': list(map(str, range(1, 8 + 1))),
        'ref1': [],
        'ref2': [],
    }


def test_respell(rep):
    assert set(rep.respellables()) == {'test2', 'test3', 'test4'}
    assert rep.respell('test2', 'hello world') == 'hll wrld'
    assert rep.respell('test3', 'hello world') == 'eo o'
    assert rep.respell('test4', 'hello world') == 'hxllx wxrld'
