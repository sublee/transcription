# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from transcription import Representation
from transcription.representation import from_yaml


def test_parse_yaml():
    yaml = '''
    name: 'test'
    normalize:
      use: ['roman_to_lower']
    define:
      vowels: {'aeiou'}
      consonants: {'qwrtypsdfghjklzxcvbnm'}
    respell:
      to: 'test2'
      pipeline:
        - '@': null
    '''
    rep = from_yaml(yaml)
    assert isinstance(rep, Representation)
