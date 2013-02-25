# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys

import pytest


pythonpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, pythonpath)


@pytest.fixture
def rep():
    from transcription import representation
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
    respell->test2:
      - '[aeiou]': null
    respell->test3:
      - '[hlwrd]': null
    respell->test4:
      - '@': 'x'
    '''
    return representation.generate_from_yaml(yaml)
