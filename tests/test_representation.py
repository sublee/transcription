# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from transcription import Representation, representation


def test_parse_yaml():
    yaml = '''
    name: 'test'
    normalize:
      use: ['roman_to_lower']
    define:
      vowels: {'aeiou'}
      consonants: {'qwrtypsdfghjklzxcvbnm'}
      all: [<vowels>, <consonants>]
      self_ref: [{1234}, <self_ref>, {5678}]
      ref1: [<ref2>]
      ref2: [<ref1>]
    respell:
      to: 'test2'
      pipeline:
        - '@': null
    '''
    rep = representation.generate_from_yaml(yaml)
    assert isinstance(rep, Representation)
    assert rep.variables == {
        'vowels': list('aeiou'),
        'consonants': list('qwrtypsdfghjklzxcvbnm'),
        'all': list('aeiouqwrtypsdfghjklzxcvbnm'),
        'self_ref': list(map(str, range(1, 8 + 1))),
        'ref1': [],
        'ref2': [],
    }
