# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from transcription.respell import Respell


def compile_pattern(pattern):
    return Respell(pattern, None).compiled_pattern.pattern


def compile_repl(repl):
    return Respell('', repl).compiled_repl


def test_compile():
    assert compile_pattern('@') == '(?:a|e|i|o|u)'
    assert compile_pattern('<vowels>') == '(?:a|e|i|o|u)'
