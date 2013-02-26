# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from conftest import rep
from transcription.respell import Respell


rep = rep()


def compile_pattern(pattern):
    return Respell(pattern, None, rep.vars).compiled_pattern.pattern


def respell(pattern, repl, text):
    return Respell(pattern, repl, rep.vars)(text)


def test_compile():
    assert compile_pattern('@') == '(?:a|e|i|o|u)'
    assert compile_pattern('<vowels>') == '(?:a|e|i|o|u)'


def test_map_var():
    assert respell('<vowels>', '<long_vowels>', 'hello') == 'hEllO'
